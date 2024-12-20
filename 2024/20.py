
import time
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

    total = 0
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            p = y, x
            for dy in range(0, cheat_distance + 1):
                for dx in range(-cheat_distance + dy if dy > 0 else 0, cheat_distance + 1 - dy):
                    op = add(p, (dy, dx))
                    if 0 <= op[0] < H and 0 <= op[1] < W and distance[p] < INF and distance[op] < INF:
                        saved = abs(distance[p] - distance[op]) - (abs(dy) + abs(dx))
                        if saved >= 100:
                            total += 1

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
