
from collections import defaultdict
import numpy as np

lines = open("input-10-test.txt").read().splitlines()
lines = open("input-10.txt").read().splitlines()
grid = np.array([list(line) for line in lines], int)
NEIGHBORS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def neighbors(p):
    return [(p[0] + dx, p[1] + dy) for (dx, dy) in NEIGHBORS]

def merge_dict(s):
    d = defaultdict(lambda: set())
    for p, sp in s:
        d[p].update(sp)
    return d

def do_part_1():
    # Dict from position to trailheads that could get here.
    x = {p: {p} for p in zip(*np.where(grid == 0))}

    for i in range(1, 10):
        next_p = set(zip(*np.where(grid == i)))
        x = merge_dict((dp, sp)
                       for (p, sp) in x.items()
                       for dp in neighbors(p)
                       if dp in next_p)

    print("Part 1:", sum(len(p) for p in x.values()))

def do_part_2():
    def move_up(m, value):
        return np.pad(m[1:], ((0, 1), (0, 0)), constant_values=value)

    def move_down(m, value):
        return np.pad(m[:-1], ((1, 0), (0, 0)), constant_values=value)

    def move_left(m, value):
        return np.pad(m[:,1:], ((0, 0), (0, 1)), constant_values=value)

    def move_right(m, value):
        return np.pad(m[:,:-1], ((0, 0), (1, 0)), constant_values=value)

    x = np.zeros(grid.shape, dtype=int)
    x[grid == 0] = 1

    for i in range(1, 10):
        x = move_up(x, 0) + move_right(x, 0) + move_down(x, 0) + move_left(x, 0)
        x[grid != i] = 0

    print("Part 2:", x.sum())

do_part_1()
do_part_2()
