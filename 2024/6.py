
import numpy as np

lines = open("input-6-test.txt").read().splitlines()
lines = open("input-6.txt").read().splitlines()

GRID = np.array([list(line) for line in lines])
HEIGHT, WIDTH = GRID.shape
GUARD = tuple(np.argwhere(GRID == "^")[0])

# Return (number of covered tiles (for part 1) or number of possible loops (for part 2),
# whether a loop was found).
def run_guard(grid, guard, part):
    dy, dx = -1, 0
    covered = np.zeros(grid.shape, dtype=bool)
    steps = set()
    loops = set()

    while True:
        covered[guard] = True
        new_guard = guard[0] + dy, guard[1] + dx

        # See if we're in a loop.
        step = guard, new_guard
        if step in steps:
            return covered.sum(), True
        steps.add(step)

        # See if we're off the grid.
        if new_guard[0] < 0 or new_guard[1] < 0 or new_guard[0] >= HEIGHT or new_guard[1] >= WIDTH:
            return covered.sum() if part == 1 else len(loops), False

        # See if we've run into an obstacle.
        if grid[new_guard] == "#":
            # Turn right.
            dy, dx = dx, -dy
        else:
            # In part 2 we pretend there's an obstacle at every step to see if
            # it might create a loop.
            if part == 2:
                grid[new_guard] = "#"
                _, looped = run_guard(grid, GUARD, 1)
                if looped:
                    loops.add(new_guard)
                grid[new_guard] = "."

            # Move to new position.
            guard = new_guard

def do_part(part):
    total, _ = run_guard(GRID, GUARD, part)
    print(f"Part {part}: {total}")

do_part(1)
do_part(2)
