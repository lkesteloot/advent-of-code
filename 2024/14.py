
import re, time
import numpy as np

lines = open("input-14-test.txt").read().splitlines(); w = 11; h = 7
lines = open("input-14.txt").read().splitlines(); w = 101; h = 103

ROBOTS = [tuple(map(int, re.findall(r'(-?\d+)', line))) for line in lines]

def make_grid(seconds):
    global ROBOTS

    grid = np.zeros((h, w), dtype=int)
    for x, y, dx, dy in ROBOTS:
        x = (x + dx*seconds) % w
        y = (y + dy*seconds) % h
        grid[y,x] += 1
    return grid

def print_grid(grid):
    for row in grid:
        print("".join("." if tile == 0 else chr(tile + 0x30) for tile in row))

def do_part(part):
    if part == 1:
        grid = make_grid(100)
        return grid[:h//2,:w//2].sum() * \
                grid[h//2+1:,:w//2].sum() * \
                grid[:h//2:,w//2+1:].sum() * \
                grid[h//2+1:,w//2+1:].sum()
    else:
        best_seconds = None
        best_same = None
        best_grid = None
        for seconds in range(w*h):
            grid = make_grid(seconds)
            same = (grid[:-1,:] == grid[1:,:]).sum() + \
                    (grid[:,:-1] == grid[:,1:]).sum()
            if best_same is None or same > best_same:
                best_same = same
                best_grid = grid
                best_seconds = seconds

        #print(best_seconds)
        #print_grid(best_grid)
        return best_seconds

def main():
    for part in [1,2]:
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
