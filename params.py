from pygame.math import Vector2
from pygame.draw import line

k = 1.9  # ZOOM koef

HEIGHT = int(360 * 2 * k)
WIDTH = int(480 * 2 * k)
VIEW_DISTANCE = int(600 * k)

FPS = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

dt = 0.05

NORM_VECTOR = Vector2(1, 0)
PI = 180
N_CARS = 15
START = (577 * k, 325 * k)

N_SENSORS = 15


class Segment:
    def __init__(self, x1, y1, x2, y2):
        self.A = Vector2(x1, y1)
        self.B = Vector2(x2, y2)

    def draw(self, srf, color=BLACK):
        line(srf, color, self.A, self.B, 3)
