
import time
from itertools import count
import numpy as np

lines = open("input-20-test.txt").read().splitlines()
lines = open("input-20.txt").read().splitlines()

DELTA = [(1, 0), (-1, 0), (0, 1), (0, -1)]
GRID = np.array([list(line) for line in lines])
H, W = GRID.shape
START = tuple(np.argwhere(GRID == "S")[0])
END = tuple(np.argwhere(GRID == "E")[0])
GRID[START] = "."
GRID[END] = "."
INF = GRID.shape[0] * GRID.shape[1]

def add(p, d):
    return p[0] + d[0], p[1] + d[1]

def first(d):
    return slice(1, -1 - d) if d >= 0 else second(-d)

def second(d):
    return slice(1 + d, -1) if d >= 0 else first(-d)

def do_part(part):
    cheat_distance = 2 if part == 1 else 20

    # Calculate distance from start, along original path.
    distance = np.full(GRID.shape, INF, dtype=int)
    p = START
    for steps in count():
        distance[p] = steps
        if p == END:
            break
        for d in DELTA:
            n = add(p, d)
            if GRID[n] == "." and distance[n] == INF:
                p = n
                break

    # Find all cheats.
    total = 0
    for dy in range(0, cheat_distance + 1):
        for dx in range(-cheat_distance + dy if dy > 0 else 0, cheat_distance + 1 - dy):
            manhattan = abs(dy) + abs(dx)
            a1 = distance[first(dy), first(dx)]
            a2 = distance[second(dy), second(dx)]
            both_open = (a1 < INF) & (a2 < INF)
            saved = np.abs(a1 - a2) - manhattan
            saved[~both_open] = 0
            total += np.count_nonzero(saved >= 100)

    return total

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
