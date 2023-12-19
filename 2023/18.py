
import sys, re

part2 = True

if False:
    lines = open("input-18-test.txt").read().splitlines()
    DELTA = dict(U=(0,-1), R=(1,0), D=(0,1), L=(-1,0))
else:
    lines = open("input-18.txt").read().splitlines()
    # Rotate 180° so that we're always starting to the right.
    DELTA = dict(D=(0,-1), L=(1,0), U=(0,1), R=(-1,0))

DIGIT_TO_DIR = {"0": "R", "1": "D", "2": "L", "3": "U"}

# Parse input.
steps = []
for line in lines:
    # R 6 (#70c710)
    d, dist, color = line.split()
    if part2:
        dist = int(color[2:7], 16)
        d = DIGIT_TO_DIR[color[7]]
    else:
        dist = int(dist)
    dx, dy = DELTA[d]
    steps.append( (dx, dy, dist) )

# Find unique X's and Y's.
xs = set()
ys = set()
x, y = 0, 0
for dx, dy, dist in steps:
    x += dx*dist
    y += dy*dist
    xs.add(x)
    ys.add(y)

# Make bidirectional map to compressed coordinates.
ix_to_x = {ix*2: x for ix, x in enumerate(sorted(xs))}
iy_to_y = {iy*2: y for iy, y in enumerate(sorted(ys))}
x_to_ix = {x: ix for ix,x in ix_to_x.items()}
y_to_iy = {y: iy for iy,y in iy_to_y.items()}

# Draw in compressed coordinates.
x, y = 0, 0
ix, iy = x_to_ix[x], y_to_iy[y]
oix, oiy = ix, iy
tiles = {(ix, iy): "#"}
for dx, dy, dist in steps:
    x2 = x + dx*dist
    y2 = y + dy*dist
    ix2 = x_to_ix[x2]
    iy2 = y_to_iy[y2]

    idist = abs(ix2 - ix) + abs(iy2 - iy)

    corner = tiles[ix, iy]
    if dy == 1:
        ch = "|"
        tiles[ix, iy] = "|" if corner == "#" else "F"
    elif dx == -1:
        ch = "-"
        tiles[ix, iy] = "#" if corner == "#" else "*"
    elif dx == 1:
        ch = "#"
        tiles[ix, iy] = "#"
    else:
        ch = "#"

    for i in range(idist):
        ix += dx
        iy += dy
        tiles[ix, iy] = ch

    x, y = x2, y2

# We always start to the right.
tiles[oix, oiy] = "#"

# Bounding box.
min_x = min(p[0] for p in tiles.keys())
min_y = min(p[1] for p in tiles.keys())
max_x = max(p[0] for p in tiles.keys())
max_y = max(p[1] for p in tiles.keys())

# Flood fill.
start_x = min(p[0] for p in tiles if p[1] == min_y) + 1
start_y = min_y + 1
queue = [(start_x, start_y)]
while queue:
    p = queue.pop()
    if p not in tiles:
        tiles[p] = "#"
        for dx, dy in DELTA.values():
            queue.append( (p[0] + dx, p[1] + dy) )

# Print.
if not part2:
    for y in range(min_y, max_y + 1):
        parts = []
        for x in range(min_x, max_x + 1):
            p = x, y
            parts.append(tiles.get(p, "."))
        print("".join(parts))

# Sum size of each compressed block.
total = 0
for (ix, iy), ch in tiles.items():
    if ix % 2 == 0 and iy % 2 == 0:
        x1 = ix_to_x[ix]
        y1 = iy_to_y[iy]
        x2 = ix_to_x.get(ix + 2)
        y2 = iy_to_y.get(iy + 2)
        dx = None if x2 is None else x2 - x1
        dy = None if y2 is None else y2 - y1
        if ch == "|":
            size = dy
        elif ch == "-":
            size = dx
        elif ch == "*":
            size = 1
        elif ch == "F":
            size = dx + dy - 1
        else:
            size = dx*dy
        total += size
print(total)
