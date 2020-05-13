import geometry
from AI import *
from pygame.draw import polygon, circle


class Car:
    def __init__(self, name, x=START[0], y=START[1]):
        self.name = name
        self.pos = Vector2(x, y)
        self.v = Vector2()
        self.tires_traces = []

        self.dir = PI

        self.fwd_spd = 40
        self.rotate_spd = 1

        self.height = 7
        self.width = 3
        self.color = BLACK

        self.ai = AI.create()
        self.dead = 0

        self.score = 0

    def move(self):
        self.pos += self.v * dt
        self.v *= 0.97

    def update_score(self, checkpoints):
        if self.collide_segment(checkpoints[self.score % len(checkpoints)]):
            self.score += 1

    def forward(self, spd):
        a = NORM_VECTOR.rotate(self.dir)
        a.scale_to_length(self.fwd_spd * spd)
        self.v += a * dt

    def turn(self, spd):
        self.dir += self.rotate_spd * spd

    def draw(self, srf):
        dx = NORM_VECTOR.rotate(self.dir)
        dx.scale_to_length(self.height)
        dy = NORM_VECTOR.rotate(self.dir).rotate(PI / 2)
        dy.scale_to_length(self.width)
        fl = self.pos + dx + dy
        fr = self.pos + dx - dy
        bl = self.pos - dx + dy
        br = self.pos - dx - dy
        polygon(srf, self.color, [fr, fl, bl, br])

    def collide(self, field):
        dx = NORM_VECTOR.rotate(self.dir)
        dx.scale_to_length(self.height)
        dy = NORM_VECTOR.rotate(self.dir).rotate(PI / 2)
        dy.scale_to_length(self.width)
        fl = self.pos + dx + dy
        fr = self.pos + dx - dy
        bl = self.pos - dx + dy
        br = self.pos - dx - dy
        my_segs = [Segment(fl.x, fl.y, fr.x, fr.y), Segment(fr.x, fr.y, bl.x, bl.y), Segment(bl.x, bl.y, br.x, br.y),
                   Segment(br.x, br.y, fl.x, fl.y)]
        for my_seg in my_segs:
            for other_seg in field:
                if geometry.intersectTwoSegments(my_seg, other_seg):
                    return True
        return False

    def collide_segment(self, segment):
        dx = NORM_VECTOR.rotate(self.dir)
        dx.scale_to_length(self.height)
        dy = NORM_VECTOR.rotate(self.dir).rotate(PI / 2)
        dy.scale_to_length(self.width)
        fl = self.pos + dx + dy
        fr = self.pos + dx - dy
        bl = self.pos - dx + dy
        br = self.pos - dx - dy
        my_segs = [Segment(fl.x, fl.y, fr.x, fr.y), Segment(fr.x, fr.y, bl.x, bl.y), Segment(bl.x, bl.y, br.x, br.y),
                   Segment(br.x, br.y, fl.x, fl.y)]
        for my_seg in my_segs:
            if geometry.intersectTwoSegments(my_seg, segment):
                return True
        return False

    def read_sensors(self, field):
        ind = 0
        sensors = np.empty(N_SENSORS)
        for deg in np.linspace(0, 2 * PI, N_SENSORS, endpoint=False):
            vector = NORM_VECTOR.rotate(self.dir).rotate(deg)
            vector.scale_to_length(VIEW_DISTANCE)
            endpoint = self.pos + vector
            rey = Segment(self.pos[0], self.pos[1], endpoint[0], endpoint[1])
            for elem in field:
                itPoint = geometry.intersectTwoSegments(elem, rey)
                if itPoint is not None:
                    rey = Segment(self.pos[0], self.pos[1], itPoint[0], itPoint[1])
            # rey.draw(screen, YELLOW)
            sensors[ind] = (rey.A - rey.B).magnitude()
            ind += 1
        return sensors

    def mutate(self, k=0.01):
        car = Car("car")
        if k == 0:
            car.ai = self.ai
            return car
        car.ai = self.ai.mutate(k)
        return car

    def update_and_show_tires_traces(self, srf):
        ANGLE_WHEN_TIRES_TRACES = 20
        START_POW = 120
        COLOR_DIFFERENCE = 1
        CIRCLE_RADIUS = 1

        dir_vect = NORM_VECTOR.rotate(self.dir % 360)
        dir_vect.scale_to_length(50)
        v_vect = Vector2(self.v[0], self.v[1])
        if v_vect.magnitude_squared() != 0:
            v_vect.scale_to_length(50)
        if abs(dir_vect.angle_to(self.v)) > ANGLE_WHEN_TIRES_TRACES:
            dx = NORM_VECTOR.rotate(self.dir)
            dx.scale_to_length(self.height)
            dy = NORM_VECTOR.rotate(self.dir).rotate(PI / 2)
            dy.scale_to_length(self.width)
            bl = self.pos - (dx + dy) * 0.8
            br = self.pos - (dx - dy) * 0.8
            self.tires_traces.append((bl, START_POW))
            self.tires_traces.append((br, START_POW))
        new_tires_traces = []
        for pos, pow in self.tires_traces:
            circle(srf, (pow, pow, pow), (int(pos[0]), int(pos[1])), CIRCLE_RADIUS)
            pow += COLOR_DIFFERENCE
            if pow < 254:
                new_tires_traces.append((pos, pow))

        self.tires_traces = new_tires_traces

    def reset(self):
        self.pos = Vector2(START[0], START[1])
        self.v = Vector2()
        self.tires_traces = []

        self.dir = PI

        self.fwd_spd = 40
        self.rotate_spd = 1

        self.height = 7
        self.width = 3
        self.color = BLACK

        self.dead = 0

        self.score = 0
