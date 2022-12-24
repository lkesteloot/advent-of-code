

# mv ~/Downloads/input.txt input-12.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

import heapq

lines = [line.strip() for line in open("input-12-test.txt")]
lines = [line.strip() for line in open("input-12.txt")]
orig_lines = lines
W = len(orig_lines[0])
H = len(orig_lines)

cache = {}  # (xx, yy) to best distance

def foo(xx, yy):
    global W, H, orig_lines, cache
    lines = [list(line) for line in orig_lines]

    heap = []
    weights = []
    E = None

    for y in range(H):
        weights.append([])
        for x in range(W):
            w = 1000000
            if lines[y][x] == 'S':
                lines[y][x] = 'a'

            if lines[y][x] == 'E':
                E = (y,x)
                lines[y][x] = 'z'

            if xx == x and yy == y:
                if lines[yy][xx] != 'a':
                    return
                w = 0

            heapq.heappush(heap, (w, y, x))
            weights[y].append(w)

    while len(heap) > 0:
        weight, y, x = heapq.heappop(heap)

        p = (x, y)
        if p in cache:
            w = cache[p]
            #return w + weight

        #print(weight, y, x)
        w = weights[y][x] + 1
        if x > 0 and ord(lines[y][x - 1]) <= ord(lines[y][x]) + 1 and w < weights[y][x - 1]:
            weights[y][x - 1] = w
            heapq.heappush(heap, (w, y, x - 1))
        if x < W - 1 and ord(lines[y][x + 1]) <= ord(lines[y][x]) + 1 and w < weights[y][x + 1]:
            weights[y][x + 1] = w
            heapq.heappush(heap, (w, y, x + 1))
        if y > 0 and ord(lines[y - 1][x]) <= ord(lines[y][x]) + 1 and w < weights[y - 1][x]:
            weights[y - 1][x] = w
            heapq.heappush(heap, (w, y - 1, x))
        if y < H - 1 and ord(lines[y + 1][x]) <= ord(lines[y][x]) + 1 and w < weights[y + 1][x]:
            weights[y + 1][x] = w
            heapq.heappush(heap, (w, y + 1, x))
        if (y, x) == E:
            return weight


min_w = 10000
for yy in range(H):
    print(yy, H)
    for xx in range(W):
        w = foo(xx, yy)
        cache[(xx,yy)] = w
        #print(xx, yy, w)
        if w is not None and w < min_w:
            min_w = w
print(min_w)
