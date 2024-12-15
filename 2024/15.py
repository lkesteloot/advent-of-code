
import time
import numpy as np

#data = open("input-15-test-1.txt").read()
#data = open("input-15-test-2.txt").read()
data = open("input-15-test-3.txt").read()
data = open("input-15.txt").read()

GRID, MOVES = data.split("\n\n")
GRID = np.array([list(line) for line in GRID.splitlines()])
MOVES = MOVES.replace("\n", "")
PLAYER = tuple(np.argwhere(GRID == "@")[0])
GRID[PLAYER] = "."

DIRS = {
    "<": (0, -1),
    ">": (0, 1),
    "^": (-1, 0),
    "v": (1, 0),
}

def print_grid(grid, p):
    grid[p] = "@"
    for row in grid:
        print("".join(row))
    grid[p] = "."

def add(p, d):
    return p[0] + d[0], p[1] + d[1]

# 1D view of grid starting and p and "size" wide.
def cells(grid, p, size):
    return grid[p[0],p[1]:p[1]+size]

# (p, size) of item containing p.
def item_at(grid, p):
    size = 1
    if grid[p] == "]":
        p = add(p, (0, -1))
        size = 2
    elif grid[p] == "[":
        size = 2
    return p, size

def do_part(part):
    if part == 1:
        grid = GRID.copy()
        player = PLAYER
    else:
        grid = np.empty((GRID.shape[0], GRID.shape[1]*2), dtype=GRID.dtype)
        grid[:,::2] = GRID
        grid[grid == "O"] = "["
        grid[:,1::2] = GRID
        grid[grid == "O"] = "]"
        player = PLAYER[0], PLAYER[1]*2

    for move in MOVES:
        d = DIRS[move]

        new_player = add(player, d)
        if grid[new_player] == ".":
            player = new_player
        elif grid[new_player] == "#":
            pass
        else:
            to_consider = {item_at(grid, new_player)}
            processed = set()

            can_move = True
            while can_move and to_consider:
                item = to_consider.pop()
                if item not in processed:
                    processed.add(item)
                    p, size = item
                    c = cells(grid, p, size)
                    old_contents = c.copy()
                    c.fill(".")
                    new_p = add(p, d)
                    new_c = cells(grid, new_p, size)
                    if (new_c == ".").all():
                        # Can move.
                        pass
                    elif (new_c == "#").any():
                        # Can't move.
                        can_move = False
                    else:
                        # Push something.
                        for i in range(size):
                            sub_p = add(new_p, (0, i))
                            if grid[sub_p] != ".":
                                to_consider.add(item_at(grid, sub_p))

                    c[:] = old_contents

            if can_move:
                to_place = []
                for p, size in processed:
                    c = cells(grid, p, size)
                    to_place.append( (add(p, d), size, c.copy()) )
                    c.fill(".")
                for p, size, old_contents in to_place:
                    cells(grid, p, size)[:] = old_contents
                player = new_player

    return sum(y*100 + x for y, x in np.argwhere((grid == "O") | (grid == "[")))

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
