
# mv ~/Downloads/input.txt input-15.txt

import sys
from collections import defaultdict
from itertools import *
from more_itertools import *
# import numpy as np
# import scipy.signal
from heapq import *

lines = [line.strip() for line in open("input-15.txt")]

risks = [list(map(int, list(line))) for line in lines]
width = len(risks[0])
height = len(risks)

new_risks = []
for y in range(height*5):
    row = []
    for x in range(width*5):
        value = risks[y % height][x % width] + (y // height) + (x // width)
        if value > 9:
            value -= 9

        row.append(value)

    new_risks.append(row)
risks = new_risks
width *= 5
height *= 5

visited = [[False]*width for i in range(height)]
dist = [[9999999]*width for i in range(height)]

dist[0][0] = 0
h = []

def check(x, y, fr):
    if x < 0 or y < 0 or x >= width or y >= height or visited[y][x]:
        return

    new = fr + risks[y][x]
    if new < dist[y][x]:
        dist[y][x] = new
        heappush(h, (new, x, y))

for x in range(width):
    for y in range(height):
        heappush(h, (99999, x, y) )
heappush(h, (0, 0, 0) )

x = 0
y = 0
while True:
    while True:
        value, x, y = heappop(h)
        if not visited[y][x]:
            break

    visited[y][x] = True
    check(x + 1, y, dist[y][x])
    check(x - 1, y, dist[y][x])
    check(x, y - 1, dist[y][x])
    check(x, y + 1, dist[y][x])

    if y == height - 1 and x == width - 1:
        print(dist[y][x])
        sys.exit(0)
