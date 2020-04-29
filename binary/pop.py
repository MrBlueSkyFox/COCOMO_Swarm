import numpy as np
import random
from metrix import MD


class Pop():
    def __init__(self, max, min, n):
        self.max = max
        self.min = min
        self.n = n
        self.vector = [random.uniform(0, 10), random.uniform(0, 10)]
        self.MD = MD(self.vector)

    def fit_func(self):
        return self.MD

    def calc_fit(self):
        self.MD = MD(self.vector)

    def to_int(self, x):
        x = float(x)
        minx = float(self.min)
        maxx = float(self.max)
        x = x - minx
        x = x / (maxx - minx)
        x = int(round(x * 2 ** self.n))
        return x

    def from_int(self, x):
        minx = float(self.min)
        maxx = float(self.max)
        x = float(x) / 2 ** self.n
        x = x * (maxx - minx)
        x = x + minx
        return x

    def __str__(self):
        ans = 'MD= ' + str(self.MD) + ' a = ' + str(self.vector[0])
        'b = ' + str(self.vector[1]) + ' \n'
        return ans
