

# mv ~/Downloads/input.txt input-15.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-15-test.txt")]
y_line = 10
max = 20
lines = [line.strip() for line in open("input-15.txt")]
y_line = 2000000
max = 4000000

mult = 4000000

s = [] # (x,y)
b = [] # (x,y)

for line in lines:
    i = line.index("x=")
    line = line[i+2:]
    i = line.index(",")
    x = int(line[:i])
    i = line.index("y=")
    line = line[i+2:]
    i = line.index(":")
    y = int(line[:i])
    s.append((x,y))

    i = line.index("x=")
    line = line[i+2:]
    i = line.index(",")
    x = int(line[:i])
    i = line.index("y=")
    line = line[i+2:]
    y = int(line)
    b.append((x,y))

#print(s)
#print(b)

def in_diamond(x, y):
    for i in range(len(s)):
        sx, sy = s[i]
        bx, by = b[i]
        max_d = abs(sx - bx) + abs(sy - by)
        d = abs(sx - x) + abs(sy - y)
        if d <= max_d:
            return True
    return False

def check(x, y):
    if x >= 0 and y >= 0 and x <= max and y <= max and not in_diamond(x, y):
        print(x, y, x*mult + y)

if False:
    for y_line in range(max + 1):
        x_set = set()
        for i in range(len(s)):
            sx, sy = s[i]
            bx, by = b[i]
            #print(sx, sy, bx, by)

            d = abs(sx - bx) + abs(sy - by)
            dy = abs(sy - y_line)

            #print(d, dy)
            if d >= dy:
                for x in range(d - dy):
                    #print(x)
                    x_set.add(sx - (x + 1))
                    x_set.add(sx + (x + 1))
                x_set.add(sx)

        for x,y in b:
            if y == y_line:
                x_set.add(x)
                pass

        ss = ""
        for x in range(max + 1):
            if x in x_set:
                ss += "#"
            else:
                ss += "."
        print(ss)

    #print(sorted(list(x_set)))
    #print(len(x_set))
else:
    for i in range(len(s)):
        print(i)
        sx, sy = s[i]
        bx, by = b[i]
        d = abs(sx - bx) + abs(sy - by)

        for dx in range(d + 2):
            y = sy - dx
            x = sx - d - 1 + dx
            check(x,y)

            x = sx + d + 1 - dx
            check(x,y)

            y = sy + dx
            x = sx - d - 1 + dx
            check(x,y)

            x = sx + d + 1 - dx
            check(x,y)

