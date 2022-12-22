
ff = open("input-22-test.txt").read()
ff = open("input-22.txt").read()

mmap, instructions = ff.split("\n\n")
mmap = mmap.split("\n")
HEIGHT = len(mmap)
WIDTH = max(len(line) for line in mmap)
part1 = WIDTH == 16
TILE = 4 if part1 else 50
instructions = instructions.strip()

for i in range(HEIGHT):
    mmap[i] = mmap[i].ljust(WIDTH)

x = len(mmap[0]) - len(mmap[0].lstrip()) + 1
y = 1
d = 0

def get_direction(d):
    if d == 0:
        dx, dy = 1, 0
    elif d == 1:
        dx, dy = 0, 1
    elif d == 2:
        dx, dy = -1, 0
    elif d == 3:
        dx, dy = 0, -1
    else:
        raise Exception()
    return dx, dy

if part1:
    EDGES = [
            (9, 1, 1, 2,   5, 5, 0, 1),
            (9, 1, 0, 3,   4, 5, 2, 1),
            (12, 1, 1, 0,  16, 12, 3, 2),
            (12, 5, 1, 0,  16, 9, 2, 1),
            (16, 12, 2, 1, 1, 5, 1, 0),
            (9, 12, 0, 1,  4, 8, 2, 3),
            (5, 8, 0, 2,   9, 9, 1, 0),
    ]
else:
    EDGES = [
            (51, 1, 0, 3,    1, 151, 1, 0),
            (101, 1, 0, 3,   1, 200, 0, 3),
            (150, 1, 1, 0,   100, 150, 3, 2),
            (150, 50, 2, 1,  100, 100, 3, 2),
            (51, 150, 0, 1,  50, 151, 1, 2),
            (1, 101, 1, 2,   51, 50, 3, 0),
            (1, 101, 0, 3,   51, 51, 1, 0),
    ]

JUMPS = {}
for x1, y1, d1, v1, x2, y2, d2, v2 in EDGES:
    dx1, dy1 = get_direction(d1)
    dx2, dy2 = get_direction(d2)
    vx1, vy1 = get_direction(v1)
    vx2, vy2 = get_direction(v2)
    for i in range(TILE):
        JUMPS[(x1, y1, v1)] = (x2, y2, v2)
        JUMPS[(x2, y2, (v2 + 2) % 4)] = (x1, y1, (v1 + 2) % 4)
        x1 += dx1
        y1 += dy1
        x2 += dx2
        y2 += dy2

count = 0

def move():
    global count, mmap, WIDTH, HEIGHT, x, y, d, JUMPS

    while count > 0:
        p = JUMPS.get((x, y, d))
        if p is not None:
            nx, ny, nd = p
        else:
            dx, dy = get_direction(d)
            nx = x + dx
            ny = y + dy
            nd = d

        if mmap[ny - 1][nx - 1] == ' ':
            raise Exception()

        if mmap[ny - 1][nx - 1] == '#':
            count = 0
            return

        x = nx
        y = ny
        d = nd
        count -= 1

i = 0
while i < len(instructions):
    ch = instructions[i]
    if ch >= "0" and ch <= "9":
        count = count*10 + ord(ch) - ord("0")
    else:
        move()
        if ch == "R":
            d = (d + 1) % 4
        elif ch == "L":
            d = (d - 1) % 4
        else:
            raise Exception(ch)
    i += 1

move()
answer = 1000*y + 4*x + d
print(answer)

