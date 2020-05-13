from utils.params import *
import numpy as np


def activation(arr):
    return np.tanh(arr)


class AI:
    INPUT = N_SENSORS
    HIDDEN = 15
    OUTPUT = 2

    def __init__(self, hid, outp):
        self.hid = hid
        self.outp = outp

    @staticmethod
    def create():
        hidden_weight = np.random.uniform(low=-0.005, high=0.005, size=(AI.INPUT, AI.HIDDEN))
        out_weight = np.random.uniform(low=-0.5, high=0.5, size=(AI.HIDDEN, AI.OUTPUT))
        return AI(hidden_weight, out_weight)

    def calculate(self, sensors):
        r1 = sensors
        r1 = np.matmul(r1, self.hid)
        r1 = activation(r1)
        r1 = np.matmul(r1, self.outp)
        r1 = activation(r1)
        forw, turn = r1[0], r1[1]
        if abs(turn) < 0.2:
            turn = 0
        else:
            turn = np.sign(turn)
        return forw, turn

    def mutate(self, k):
        ai = AI(self.hid.copy(), self.outp.copy())
        ai.hid += np.random.uniform(-k / AI.INPUT, k / AI.INPUT, size=ai.hid.shape)
        ai.outp += np.random.uniform(-k / AI.HIDDEN, k / AI.HIDDEN, size=ai.outp.shape)
        return ai

    def write(self, filename):
        with open(filename, "w") as f:
            for line in self.hid:
                print(*line, file=f)
            for line in self.outp:
                print(*line, file=f)

    def read(self, filename):
        with open(filename, "r") as f:
            hid = np.empty(shape=(AI.INPUT, AI.HIDDEN))
            outp = np.empty(shape=(AI.HIDDEN, AI.OUTPUT))
            for i in range(AI.INPUT):
                line = np.array(list(map(float, f.readline().split())))
                hid[i] = line
            for i in range(AI.HIDDEN):
                line = np.array(list(map(float, f.readline().split())))
                outp[i] = line
        self.hid = hid
        self.outp = outp
