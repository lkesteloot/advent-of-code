
import time
import numpy as np

lines = open("input-12-test.txt").read().splitlines()
#lines = open("input-12.txt").read().splitlines()

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

def separate_parts(grid):
    new_grid = np.empty(grid.shape, dtype=int)
    to_do = {(y,x) for x in range(w) for y in range(h)}

    counter = 0
    while to_do:
        p = to_do.pop()
        ps = flood_fill(p)
        to_do -= ps
        for p in ps:
            new_grid[p] = counter
        counter += 1

    return new_grid, counter


def do_part_x(part):
    new_grid, counter = separate_parts(grid)

    vert = (new_grid[1:,1:-1] != new_grid[:-1,1:-1]).astype(int)
    horiz = (new_grid[1:-1,1:] != new_grid[1:-1,:-1]).astype(int)

    new_grid = new_grid[1:-1,1:-1]
    print(new_grid)
    #print(vert)
    #print(horiz)
    is_top = vert[:-1,:]
    is_bottom = vert[1:,:]
    is_left = horiz[:,:-1]
    is_right = horiz[:,1:]
    print(is_top)
    #print(is_right)
    #print(is_bottom)
    #print(is_left)

    area_grid = np.empty(new_grid.shape, dtype=int)
    for i in range(0, counter):
        where = new_grid == i
        area_grid[where] = where.sum()
    #print("Area")
    #print(area_grid)

    if part == 1:
        edges = is_top + is_right + is_bottom + is_left
        #print("Edges")
        #print(edges)
    else:

    total = (area_grid*edges).sum()

    return total


def main():
    for part in [1, 2, 3, 4]:
        before = time.perf_counter()
        answer = do_part(part) if part <= 2 else do_part_x(part - 2)
        after = time.perf_counter()
        elapsed = round((after - before)*1_000_000)
        unit = "µs"
        if elapsed >= 1000:
            elapsed //= 1000
            unit = "ms"
        print(f"Part {part}: {answer} ({elapsed:,} {unit})")

main()
