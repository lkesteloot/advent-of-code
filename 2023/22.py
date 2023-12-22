
from collections import defaultdict

lines = open("input-22.txt").read().splitlines()

# Parse.
bricks = []
for line in lines:
    begin, end = line.split("~")
    begin = tuple(map(int, begin.split(",")))
    end = tuple(map(int, end.split(",")))
    bricks.append( (begin, end) )

# Sort by Z.
bricks.sort(key=lambda p: p[0][2])

# Iterate over x,y coords of a brick.
def coords(begin, end):
    for x in range(begin[0], end[0] + 1):
        for y in range(begin[1], end[1] + 1):
            yield x, y

# Height off the ground of all the bricks dropped so far.
height = defaultdict(int)

# Drop the bricks.
dropped_bricks = []
for begin, end in bricks:
    max_z = max(height[x, y] for x, y in coords(begin, end))
    drop = begin[2] - (max_z + 1)
    assert drop >= 0
    for x, y in coords(begin, end):
        height[x, y] = end[2] - drop
    dropped_bricks.append( ((begin[0], begin[1], begin[2] - drop), (end[0], end[1], end[2] - drop)) )
bricks = dropped_bricks

# Map from height to bricks whose top is height.
tops_at = defaultdict(list)
for i, (begin, end) in enumerate(bricks):
    tops_at[end[2]].append( (begin, end, i) )

# Whether two 1D extents overlap.
def overlaps1d(begin1, end1, begin2, end2):
    return not (end1 < begin2 or end2 < begin1)

# Whether two 2D extents overlap.
def overlaps2d(begin1, end1, begin2, end2):
    return overlaps1d(begin1[0], end1[0], begin2[0], end2[0]) and \
           overlaps1d(begin1[1], end1[1], begin2[1], end2[1])

# Build graph of who is supporting and supported by who.
supports = {i: set() for i in range(len(bricks))}
supported_by = {i: set() for i in range(len(bricks))}
for i, (begin1, end1) in enumerate(bricks):
    for begin2, end2, j in tops_at[begin1[2] - 1]:
        if overlaps2d(begin1, end1, begin2, end2):
            supports[j].add(i)
            supported_by[i].add(j)

# Number of bricks that would be destroyed if "i" were destroyed.
def would_be_destroyed(i, supported_by):
    # Deep copy.
    supported_by = dict((a, set(b)) for a, b in supported_by.items())
    destroyed = set()
    to_destroy = {i}

    while to_destroy:
        i = to_destroy.pop()
        destroyed.add(i)

        for j in supports[i]:
            supported_by[j] -= {i}
            if len(supported_by[j]) == 0:
                to_destroy.add(j)

    return len(destroyed - {i})

print("part1", sum(1 for i in range(len(bricks)) if would_be_destroyed(i, supported_by) == 0))
print("part2", sum(would_be_destroyed(i, supported_by) for i in range(len(bricks))))

