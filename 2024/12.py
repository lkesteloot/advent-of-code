
import time
import numpy as np

lines = open("input-12-test.txt").read().splitlines()
lines = open("input-12.txt").read().splitlines()

grid = np.array([list(line) for line in lines])
grid = np.pad(grid, 1, constant_values=".")
w, h = grid.shape

def neighbors(p):
    y, x = p
    return [
        (y + 1, x),
        (y - 1, x),
        (y, x + 1),
        (y, x - 1),
    ]

def flood_fill(p):
    ch = grid[p]
    ps = set()
    to_do = {p}

    while to_do:
        p = to_do.pop()
        y, x = p
        if 0 <= x < w and 0 <= y < h and grid[p] == ch and p not in ps:
            ps.add(p)
            to_do.update(neighbors(p))

    return ps

def count_tops(ps):
    ls = sorted(ps)
    prev = (-1, -1)
    sides = 0
    for p in ls:
        if (p[0] - 1, p[1]) not in ps:
            if p != (prev[0], prev[1] + 1):
                sides += 1
            prev = p
        else:
            prev = (-1, -1)
    return sides

def rotate_point(p):
    y, x = p
    return x, h - 1 - y

def rotate_set(ps):
    return set(rotate_point(p) for p in ps)

def count_sides(ps):
    total = count_tops(ps)
    ps = rotate_set(ps)
    total += count_tops(ps)
    ps = rotate_set(ps)
    total += count_tops(ps)
    ps = rotate_set(ps)
    total += count_tops(ps)

    return total

def do_part(part):
    total = 0
    to_do = {(y,x) for x in range(w) for y in range(h)}

    while to_do:
        p = to_do.pop()
        ch = grid[p]
        ps = flood_fill(p)
        to_do -= ps
        if ch != ".":
            area = len(ps)
            if part == 1:
                perimeter = sum(sum(grid[n] != ch for n in neighbors(p)) for p in ps)
            else:
                perimeter = count_sides(ps)
            total += area*perimeter

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
