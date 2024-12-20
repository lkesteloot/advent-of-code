
import time
from collections import Counter
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

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def print_grid(grid):
    for row in grid:
        print("".join(str(tile) for tile in row))

def do_part(part):
    cheat_distance = 2 if part == 1 else 20

    distance = np.full(GRID.shape, INF, dtype=int)

    steps = 0
    p = START
    while True:
        distance[p] = steps
        if p == END:
            break

        for d in DELTA:
            n = add(p, d)
            if GRID[n] == "." and distance[n] == INF:
                p = n
                break
        else:
            raise Exception()

        steps += 1

    default_distance = distance[END]

    def determine_saved(p1, p2):
        return abs(distance[p1] - distance[p2]) - manhattan(p1, p2)

    saved_counter = Counter()

    total = 0
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            p = y, x
            for dy in range(0, cheat_distance + 1):
                for dx in range(-cheat_distance if dy > 0 else 0, cheat_distance + 1):
                    if abs(dx) + abs(dy) <= cheat_distance:
                        op = add(p, (dy, dx))
                        if 0 <= op[0] < H and 0 <= op[1] < W:
                            if GRID[p] == "." and GRID[op] == ".":
                                saved = determine_saved(p, op)
                                saved_counter[saved] += 1
                                if saved >= 100:
                                    total += 1

    if False:
        print(saved_counter)
        for saved in sorted(saved_counter.keys()):
            print(saved_counter[saved], "cheats that save", saved)

    # it's 1033983
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
