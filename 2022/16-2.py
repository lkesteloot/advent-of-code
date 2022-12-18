
# mv ~/Downloads/input.txt input-16.txt

import sys
import re
from collections import defaultdict, Counter, deque
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-16-test.txt")]
#lines = [line.strip() for line in open("input-16.txt")]

class Valve:
    def __init__(self, name, flow, neighbors):
        self.name = name
        self.flow = flow
        self.neighbors = neighbors

aa = None
vs = {}
for line in lines:
    # Valve HH has flow rate=22; tunnel leads to valve GG
    name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
    v = Valve(name, int(flow), neighbors)
    if name == "AA":
        aa = v
    vs[name] = v

def get_dist(start_name):
    q = deque([(start_name, 0)])
    d = {}
    while q:
        name, dist = q.popleft()
        neighbors = vs[name].neighbors
        for n in neighbors:
            if n not in d:
                d[n] = dist + 1
                q.append((n, dist + 1))

    del d[start_name]
    d = {n: d for n, d in d.items() if vs[n].flow > 0}

    return d

# Precompute distance to every other flowable node.
dists = {}
for name in vs:
    dists[name] = get_dist(name)

def get_pressure_from_room(name, opened, time_left):
    if time_left <= 2:
        return 0

    pressure = 0
    for new_name, dist in dists[name].items():
        if new_name not in opened and dist + 1 < time_left:
            this_opened = opened + [new_name]
            new_pressure = (time_left - dist - 1)*vs[new_name].flow
            p = new_pressure + get_pressure_from_room(new_name, this_opened, time_left - dist - 1)
            if p > pressure:
                pressure = p

    return pressure

pressure = get_pressure_from_room(aa.name, [], 30)
print(pressure)

