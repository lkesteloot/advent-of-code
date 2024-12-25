
import time
import numpy as np

data = open("input-25-test.txt").read()
data = open("input-25.txt").read()

LOCKS = []
KEYS = []
for section in data.split("\n\n"):
    grid = np.array([list(line) for line in section.splitlines()]) == "#"
    heights = grid.sum(axis=0) - 1
    if grid[0,0]:
        LOCKS.append(heights)
    else:
        KEYS.append(heights)

def do_part(part):
    total = 0
    if part == 1:
        for lock in LOCKS:
            for key in KEYS:
                if np.all(lock + key <= 5):
                    total += 1
    return total

def main():
    for part in [1]:
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
