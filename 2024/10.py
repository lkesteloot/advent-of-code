
import time
from collections import defaultdict
import numpy as np

lines = open("input-10-test.txt").read().splitlines()
lines = open("input-10.txt").read().splitlines()
GRID = np.array([list(line) for line in lines], int)
GRID = np.pad(GRID, 1, constant_values=-1)
NEIGHBORS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def neighbors(p):
    return ((p[0] + dx, p[1] + dy) for (dx, dy) in NEIGHBORS)

def merge_dict(s):
    d = defaultdict(set)
    for p, sp in s:
        d[p].update(sp)
    return d

def do_part_1():
    # Dict from position to trailheads that could get here.
    x = {p: {p[0] + p[1]*1000} for p in zip(*np.where(GRID == 0))}

    for i in range(1, 10):
        x = merge_dict((dp, sp)
                       for p, sp in x.items()
                       for dp in neighbors(p)
                       if GRID[dp[0], dp[1]] == i)

    return sum(map(len, x.values()))

def do_part_2():
    x = np.zeros(GRID.shape, dtype=int)
    x[GRID == 0] = 1

    for i in range(1, 10):
        x[1:-1,1:-1] = x[2:,1:-1] + x[:-2,1:-1] + x[1:-1,2:] + x[1:-1,:-2]
        x[GRID != i] = 0

    return x.sum()

def do_part(part):
    return do_part_1() if part == 1 else do_part_2()

def main():
    for part in [1, 2]:
        before = time.perf_counter()
        answer = do_part(part)
        after = time.perf_counter()
        elapsed = round((after - before)*1_000_000)
        unit = "µs"
        if elapsed >= 1000:
            elapsed //= 1000
            unit = "ms"
        print(f"Part {part}: {answer} ({elapsed:,} {unit})")

main()
