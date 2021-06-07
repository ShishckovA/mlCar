import random

import pygame
from utils.Car import *


def draw_field(srf):
    for elem in field:
        elem.draw(srf)
    if DRAW_CHECKPOINTS:
        for i, elem in enumerate(checkpoints):
            color = GREEN
            if i == 0:
                color = BLUE
            elem.draw(srf, color)


def handle_events():
    global spos, epos, EPOCHE_LEN
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if mode == 'learning':
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     spos = event.pos
            #
            # if event.type == pygame.MOUSEBUTTONUP:
            #     epos = event.pos
            #
            #     print(spos[0] / k, spos[1] / k, epos[0] / k, epos[1] / k)
            #     field.append(Segment(spos[0], spos[1], epos[0], epos[1]))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    EPOCHE_LEN += 100
                if event.key == pygame.K_DOWN:
                    EPOCHE_LEN -= 100
                pygame.display.set_caption("Epoche len: " + str(EPOCHE_LEN))


def epoche(cars):
    for car in cars:
        car.score = 0
    dead = False
    i = 0
    while i < EPOCHE_LEN:
        if dead:
            break

        screen.fill(WHITE)
        dead = True
        for car in cars:
            car.draw(screen)
            if mode == 'presentation':
                car.update_and_show_tires_traces(screen)
            if car.dead:
                continue
            dead = False
            if car.collide(field):
                car.dead = True
            car.move()
            car.update_score(checkpoints)
            fwd, trn = car.ai.calculate(car.read_sensors(field))
            car.forward(fwd)
            car.turn(trn)

        draw_field(screen)

        handle_events()
        pygame.display.update()
        if mode == "presentation":
            clock.tick(FPS)
        i += 1


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CARS WITH AI")
clock = pygame.time.Clock()

pygame.display.update()

field = []
with open("data/field.txt", "r") as f:
    for line in f.readlines():
        p1, p2, p3, p4 = map(int, line.split())
        field.append(Segment(p1 * k, p2 * k, p3 * k, p4 * k))

checkpoints = []
with open("data/checkpoints.txt", "r") as f:
    for line in f.readlines():
        p1, p2, p3, p4 = map(int, line.split())
        checkpoints.append(Segment(p1 * k, p2 * k, p3 * k, p4 * k))

field.append(Segment(0, 0, 0, HEIGHT))
field.append(Segment(0, HEIGHT, WIDTH, HEIGHT))
field.append(Segment(WIDTH, HEIGHT, WIDTH, 0))
field.append(Segment(WIDTH, 0, 0, 0))
cars = [Car("Car") for _ in range(N_CARS)]
# car = Car("car")
# car.ai.read("data/net_koef.txt")
# cars = [car]
# mode = 'presentation'
mode = 'learning'

if mode == 'presentation':
    EPOCHE_LEN = -1
    DRAW_CHECKPOINTS = False
    SHOW_TIRES_TRACE = True
    pygame.display.set_caption("Cars with AI")
elif mode == 'learning':
    EPOCHE_LEN = 300
    DRAW_CHECKPOINTS = True
    pygame.display.set_caption("Epoche len: " + str(EPOCHE_LEN))
    SHOW_TIRES_TRACE = False
else:
    print("Unknown mode")
    exit(0)

while True:
    epoche(cars)
    if mode == 'learning':
        cars.sort(key=lambda x: -x.score)
        cars[0].ai.write("data/net_koef.txt")
        print("Best score with EPOCHE_LEN = {}:".format(EPOCHE_LEN), cars[0].score)
        new_cars = []
        for i in range(min(4, len(cars))):
            cars[i].reset()
            new_cars.append(cars[i])
            new_cars.append(cars[i].mutate(0.0003))
            new_cars.append(cars[i].mutate(0.0005))
            new_cars.append(cars[i].mutate(0.001))
            # new_cars.append(cars[i].mutate(0.003))
            # new_cars.append(cars[i].mutate(0.01))
            # new_cars.append(cars[i].mutate(0.05))
            # new_cars.append(cars[i].mutate(0.1))
        cars = new_cars[:N_CARS]
        cars[0].color = RED
        random.shuffle(cars)
    elif mode == 'presentation':
        cars[0].reset()
