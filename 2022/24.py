
from collections import defaultdict
import heapq

lines = [line.strip() for line in open("input-24-test.txt")]
#lines = [line.strip() for line in open("input-24.txt")]

blizzards = defaultdict(lambda: [])  # (x, y) -> [(dx, dy)]

WIDTH = len(lines[0]) - 2
HEIGHT = len(lines) - 2

DIR = {
        "v": (0, 1),
        ">": (1, 0),
        "<": (-1, 0),
        "^": (0, -1),
}
RDIR = {}
for ch, delta in DIR.items():
    RDIR[delta] = ch

lines = lines[1:-1]

y = 0
for line in lines:
    dots = list(line)[1:-1]
    x = 0
    for dot in dots:
        if dot != ".":
            dx, dy = DIR[dot]
            blizzards[(x, y)].append((dx, dy))
        x += 1
    y += 1

def print_blizzards(b):
    print("# " + "#"*WIDTH)
    for y in range(HEIGHT):
        s = "#"
        for x in range(WIDTH):
            p = b.get((x, y))
            if p is None:
                s += "."
            elif len(p) > 1:
                s += chr(len(p) + ord("0"))
            else:
                s += RDIR[p[0]]
        s += "#"
        print(s)
    print("#"*WIDTH + " #")

def get_next_blizzard(blizzards):
    new_blizzards = defaultdict(lambda: [])
    for (ox, oy), p in blizzards.items():
        for dx, dy in p:
            x, y = ox + dx, oy + dy
            if x == WIDTH:
                x = 0
            elif x == -1:
                x = WIDTH - 1
            elif y == HEIGHT:
                y = 0
            elif y == -1:
                y = HEIGHT - 1
            new_blizzards[(x, y)].append((dx, dy))
    return new_blizzards

#print_blizzards(blizzards)

grid = set()  # (t, x, y) open space

b = blizzards
for t in range(1000):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) not in b:
                grid.add((t, x, y))
    grid.add((t, 0, -1))
    grid.add((t, WIDTH - 1, HEIGHT))
    b = get_next_blizzard(b)

start_times = [0]
total = 0
for qq in range(3):
    heap = [] # (d, t, x, y)
    dists = {} # (t,x,y) -> d
    for t, x, y in grid:
        dists[(t, x, y)] = 100000

    if qq == 0 or qq == 2:
        start = (0, -1)
        end = (WIDTH - 1, HEIGHT)
    else:
        start = (WIDTH - 1, HEIGHT)
        end = (0, -1)
    start_time = start_times[qq]
    heapq.heappush(heap, (0, start_time, start[0], start[1]))
    dists[(start_time, start[0], start[1])] = 0

    HOPS = [
            (0, 0),
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
    ]

    done = False
    while len(heap) > 0 and not done:
        d, t, x, y = heapq.heappop(heap)
        #print(d, t, x, y)
        nd = d + 1
        nt = t + 1
        for dx, dy in HOPS:
            nx, ny = x + dx, y + dy
            od = dists.get((nt, nx, ny))
            if od is not None and nd < od:
                #print("    ", nx, ny, od)
                dists[(nt, nx, ny)] = nd
                heapq.heappush(heap, (nd, nt, nx, ny))
            else:
                #print("  X ", nx, ny)
                pass

            if nx == end[0] and ny == end[1]:
                print("FOUND", nd)
                start_times.append(sum(start_times) + nd)
                total += nd
                done = True
                break

print("SOLUTION", total)
