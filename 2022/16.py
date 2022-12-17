
# mv ~/Downloads/input.txt input-16.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-16-test.txt")]
lines = [line.strip() for line in open("input-16.txt")]
# matrix = [list(map(int, list(line))) for line in lines]

class Valve:
    def __init__(self, name, flow, neighbors):
        self.name = name
        self.flow = flow
        self.neighbors = neighbors

class State:
    def __init__(self, start, opened, time_left):
        self.start = start
        self.opened = tuple(opened)
        self.time_left = time_left

    def __eq__(self, o):
        return self.start == o.start and \
                self.opened == o.opened and \
                self.time_left == o.time_left

    def __hash__(self):
        return hash((self.start, self.opened, self.time_left))

aa = None
vs = {}
for line in lines:
    line = line[6:]
    name = line[:2]
    line = line[17:]
    i = line.index(";")
    flow = int(line[:i])
    i = line.index("valve")
    line = line[i+6:].strip()
    neighbors = line.split(", ")
    v = Valve(name, flow, neighbors)
    if name == "AA":
        aa = v
    vs[name] = v

# State to pressure
cache = {}

max_pressure = 0
def get_pressure_from_room(name, opened, time_left, from_name, path):
    global max_pressure

    v = vs[name]

    state = State(v.name, opened, time_left)
    pressure = cache.get(state)
    if pressure is not None:
        return pressure

    if time_left <= 1:
        return 0

    path = path + [v.name]

    pressure = 0
    if time_left >= 2:
        for n in v.neighbors:
            if v.flow == 0 and from_name == n:
                continue
            p = get_pressure_from_room(vs[n].name, opened, time_left - 1, v.name, path)
            if p > pressure:
                pressure = p

    if v.flow != 0 and v.name not in opened:
        opened = opened + [v.name]
        time_left -= 1
        our_pressure = v.flow*time_left
        path = path + ["+" + str(v.flow*time_left)]

        pressure = max(our_pressure, pressure)
        if time_left >= 2:
            for n in v.neighbors:
                if v.flow == 0 and from_name == n:
                    continue
                p = get_pressure_from_room(vs[n].name, opened, time_left - 1, v.name, path)
                if p + our_pressure > pressure:
                    pressure = p + our_pressure

    cache[state] = pressure
    return pressure

pressure = get_pressure_from_room(aa.name, [], 30, None, [])
print(pressure, len(cache))

