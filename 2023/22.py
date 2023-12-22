
from collections import defaultdict

lines = open("input-22.txt").read().splitlines()

# Parse.
bricks = []
for line in lines:
    begin, end = line.split("~")
    begin = tuple(map(int, begin.split(",")))
    end = tuple(map(int, end.split(",")))
    bricks.append( (begin, end) )

# Sort by bottom Z.
bricks.sort(key=lambda p: p[0][2])

# Generate x,y coords of a brick.
def coords(begin, end):
    for x in range(begin[0], end[0] + 1):
        for y in range(begin[1], end[1] + 1):
            yield x, y

# Returns dropped bricks and the number of bricks whose positions changed.
def drop(bricks):
    # Height off the ground of all the bricks dropped so far.
    height = defaultdict(int)

    # Drop the bricks.
    dropped_bricks = []
    num_moved_bricks = 0
    for begin, end in bricks:
        # Max height below this brick.
        max_z = max(height[x, y] for x, y in coords(begin, end))

        # Record new top.
        drop = begin[2] - (max_z + 1)
        for x, y in coords(begin, end):
            height[x, y] = end[2] - drop

        # Move the brick down.
        if drop > 0:
            dropped_bricks.append( ((begin[0], begin[1], begin[2] - drop),
                                    (end[0], end[1], end[2] - drop)) )
            num_moved_bricks += 1
        else:
            dropped_bricks.append( (begin, end) )

    return dropped_bricks, num_moved_bricks

# Initial drop.
bricks, _ = drop(bricks)

# Number of bricks that would be destroyed if "i" were destroyed (not including "i").
def would_be_destroyed(i):
    _, num_moved_bricks = drop(bricks[:i] + bricks[i + 1:])
    return num_moved_bricks

destroyed = [would_be_destroyed(i) for i in range(len(bricks))]
print("part 1", sum(d == 0 for d in destroyed))
print("part 2", sum(destroyed))

