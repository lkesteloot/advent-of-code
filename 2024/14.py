
import re, time
import numpy as np

LINES = open("input-14-test.txt").read().splitlines(); W = 11; H = 7
LINES = open("input-14.txt").read().splitlines(); W = 101; H = 103

X, Y, DX, DY = np.array([tuple(map(int, re.findall(r'(-?\d+)', line))) for line in LINES], int).T

def make_grid(seconds):
    global X, Y, DX, DY

    x = (X + DX*seconds) % W
    y = (Y + DY*seconds) % H

    grid = np.zeros((H, W), dtype=int)
    np.add.at(grid, (y,x), 1)

    return grid

def print_grid(grid):
    for row in grid:
        print("".join("." if tile == 0 else str(tile) for tile in row))

def do_part(part):
    if part == 1:
        grid = make_grid(100)
        return grid[:H//2,:W//2].sum() * \
                grid[H//2+1:,:W//2].sum() * \
                grid[:H//2:,W//2+1:].sum() * \
                grid[H//2+1:,W//2+1:].sum()
    else:
        best_seconds = None
        best_same = None
        best_grid = None
        for seconds in range(W*H):
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
