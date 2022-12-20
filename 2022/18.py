
from collections import defaultdict

lines = [line.strip() for line in open("input-18-test.txt")]
#lines = [line.strip() for line in open("input-18.txt")]

# key is (x, y, z, axis) and side is at +1 in that axis.
sides = defaultdict(lambda: 0)
# set of all blocks (x, y, z)
blocks = set()

surface = 0

min_p = (1000, 1000, 1000)
max_p = (-1000, -1000, -1000)

def neighbors_of(p):
    x, y, z = p

    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]

def set_block(x, y, z):
    global sides, blocks, surface, min_p, max_p
    sides[(x - 1, y, z, 0)] += 1
    sides[(x, y, z, 0)] += 1
    sides[(x, y - 1, z, 1)] += 1
    sides[(x, y, z, 1)] += 1
    sides[(x, y, z - 1, 2)] += 1
    sides[(x, y, z, 2)] += 1
    blocks.add((x, y, z))
    min_p = (min(min_p[0], x), min(min_p[1], y), min(min_p[2], z))
    max_p = (max(max_p[0], x), max(max_p[1], y), max(max_p[2], z))
    surface += 6

# return True if inside.
def flood(p, flooded_blocks):
    global blocks, min_p, max_p

    if p in blocks or p in flooded_blocks:
        return True
    if p[0] > max_p[0] or \
        p[1] > max_p[1] or \
        p[2] > max_p[2] or \
        p[0] < min_p[0] or \
        p[1] < min_p[1] or \
        p[2] < min_p[2]:
            return False

    flooded_blocks.add(p)

    for n in neighbors_of(p):
        inside = flood(n, flooded_blocks)
        if not inside:
            return False

    return True

for line in lines:
    x, y, z = map(int, line.split(","))
    set_block(x, y, z)

for p in list(blocks):
    for n in neighbors_of(p):
        flooded_blocks = set()
        inside = flood(n, flooded_blocks)
        if inside:
            for block in flooded_blocks:
                set_block(*block)

for count in sides.values():
    if count == 2:
        surface -= 2

print(surface)

