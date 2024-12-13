
import time
import numpy as np

lines = open("input-12-test.txt").read().splitlines()
lines = open("input-12.txt").read().splitlines()

GRID = np.array([list(line) for line in lines])
GRID = np.pad(GRID, 1, constant_values=".")
w, h = GRID.shape

def neighbors(p):
    y, x = p
    return [
        (y + 1, x),
        (y - 1, x),
        (y, x + 1),
        (y, x - 1),
    ]

def flood_fill(p):
    ch = GRID[p]
    ps = set()
    to_do = {p}

    while to_do:
        p = to_do.pop()
        y, x = p
        if 0 <= x < w and 0 <= y < h and GRID[p] == ch and p not in ps:
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
        ch = GRID[p]
        ps = flood_fill(p)
        to_do -= ps
        if ch != ".":
            area = len(ps)
            if part == 1:
                perimeter = sum(sum(GRID[n] != ch for n in neighbors(p)) for p in ps)
            else:
                perimeter = count_sides(ps)
            total += area*perimeter

    return total

def separate_parts(grid):
    separated_grid = np.empty(grid.shape, dtype=int)
    to_do = {(y,x) for x in range(w) for y in range(h)}

    counter = 0
    while to_do:
        p = to_do.pop()
        ps = flood_fill(p)
        to_do -= ps
        for p in ps:
            separated_grid[p] = counter
        counter += 1

    return separated_grid, counter

def do_part_numpy():
    grid, counter = separate_parts(GRID)

    vert = (grid[1:,1:-1] != grid[:-1,1:-1]).astype(int)
    horiz = (grid[1:-1,1:] != grid[1:-1,:-1]).astype(int)
    diag_se = (grid[:-1,:-1] == grid[1:,1:]).astype(int)
    diag_ne = (grid[1:,:-1] == grid[:-1,1:]).astype(int)

    grid = grid[1:-1,1:-1]
    is_top = vert[:-1,:]
    is_bottom = vert[1:,:]
    is_left = horiz[:,:-1]
    is_right = horiz[:,1:]
    is_same_se = diag_se[1:,1:]
    is_same_nw = diag_se[:-1,:-1]
    is_same_sw = diag_ne[1:,:-1]
    is_same_ne = diag_ne[:-1,1:]

    area_grid = np.empty(grid.shape, dtype=int)
    for i in range(0, counter):
        where = grid == i
        area_grid[where] = where.sum()

    perimeter = is_top + is_right + is_bottom + is_left
    edges = (is_top & is_right) + \
            (is_top & (1 - is_right) & is_same_ne) + \
            (is_right & is_bottom) + \
            (is_right & (1 - is_bottom) & is_same_se) + \
            (is_bottom & is_left) + \
            (is_bottom & (1 - is_left) & is_same_sw) + \
            (is_left & is_top) + \
            (is_left & (1 - is_top) & is_same_nw)

    return (area_grid*perimeter).sum(), (area_grid*edges).sum()

def elapsed(before, after):
    elapsed = round((after - before)*1_000_000)
    unit = "µs"
    if elapsed >= 1000:
        elapsed //= 1000
        unit = "ms"
    return f"{elapsed:,} {unit}"

def main():
    for part in [1, 2]:
        before = time.perf_counter()
        answer = do_part(part)
        after = time.perf_counter()
        print(f"Part {part}: {answer} ({elapsed(before, after)})")

    before = time.perf_counter()
    answer1, answer2 = do_part_numpy()
    after = time.perf_counter()
    print(f"Parts 1 and 2: {answer1} {answer2} ({elapsed(before, after)})")

main()
