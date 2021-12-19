
# mv ~/Downloads/input.txt input-19.txt

import sys
from collections import defaultdict
from itertools import *
from functools import *
from more_itertools import *
# import numpy as np
# import scipy.signal

def orient(o, p):
    # o = 0..23
    neg = o // 12  # 0 or 1
    o %= 12
    r = o % 4   # 0, 1, 2, 3
    a = o // 4  # 0, 1, 2

    if a == 0:
        # x = x
        pass
    elif a == 1:
        # y = x
        p = (-p[1], p[0], p[2])
    else:
        # z = x
        p = (-p[2], p[1], p[0])

    if neg:
        p = (-p[0], p[1], -p[2])

    if r == 0:
        pass
    elif r == 1:
        p = (p[0], p[2], -p[1])
    elif r == 2:
        p = (p[0], p[2], -p[1])
        p = (p[0], p[2], -p[1])
    else:
        p = (p[0], p[2], -p[1])
        p = (p[0], p[2], -p[1])
        p = (p[0], p[2], -p[1])

    return p

if False:
    p = (1, 2, 3)
    for o in range(24):
        print(o, orient(o, p))
    sys.exit(0)

class Scanner:
    def __init__(self, name):
        self.name = name
        self.beacons = []
        self.d = None

    def __repr__(self):
        return self.name + ": " + repr(self.beacons)

    def get_points(self, o):
        return [orient(o, p) for p in self.beacons]

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1], p1[2] + p2[2])

def sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])

lines = [line.strip() for line in open("input-19.txt")]

s = None
scanners = []
for line in lines:
    if line.startswith("--"):
        s = Scanner(line[4:-4])
        scanners.append(s)
    elif line == "":
        pass
    else:
        p = tuple(map(int, line.split(",")))
        s.beacons.append(p)

if False:
    s1 = scanners[0]
    for s2 in scanners:
        print("---")
        for o in range(24):
            s2_points = s2.get_points(o)
            if s1.beacons == s2_points:
                neg = o // 12  # 0 or 1
                xo = o % 12
                r = xo % 4   # 0, 1, 2, 3
                a = xo // 4  # 0, 1, 2
                print(o, neg, r, a)
    sys.exit(0)

all_beacons = set()
s1 = scanners[0]
s1.d = (0, 0, 0)
s1_point_set = set(s1.beacons)
all_beacons.update(s1_point_set)
added = True
while added:
    print("Looping", len(all_beacons))
    added = False
    for s2 in scanners[1:]:
        if s2.d is not None:
            continue
        print("Considering %s (%d beacons)" % (s2.name, len(s2.beacons)))
        for o in range(24):
            if s2.d is not None:
                break
            s2_points = s2.get_points(o)
            for p1 in all_beacons:
                for p2 in s2_points:
                    d = sub(p1, p2)
                    s2_tx_points = [add(p, d) for p in s2_points]
                    c = sum(1 for p in s2_tx_points if p in all_beacons)
                    if c >= 12 and s2.d is None:
                        s2.d = d
                        #print(list(p for p in s2_tx_points if p in all_beacons))
                        all_beacons.update(s2_tx_points)
                        print(o, s2.name, d, "now", len(all_beacons))
                        added = True
                        break
                if s2.d is not None:
                    break

for s in scanners:
    print(s.d)
max_d = 0
for s1 in scanners:
    for s2 in scanners:
        d = sum(map(abs, sub(s1.d, s2.d)))
        max_d = max(max_d, d)
print(len(all_beacons), max_d)
