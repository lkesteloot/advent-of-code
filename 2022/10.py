

# mv ~/Downloads/input.txt input-10.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-10-test.txt")]
lines = [line.strip() for line in open("input-10.txt")]
# matrix = [list(map(int, list(line))) for line in lines]

W = 40
H = 6
cycle = 0
x = 1
total = 0

row = 0
col = 0

def check():
    global cycle, x, total, col, row

    if False and cycle in [20, 60, 100, 140, 180, 220]:
        v = cycle*x
        print(cycle, x, v)
        total += v

    if abs(col - x) <= 1:
        ch = "#"
    else:
        ch = "."
    sys.stdout.write(ch)

    col += 1
    if col == W:
        col = 0
        row += 1
        sys.stdout.write("\n")


for line in lines:
    if line == "noop":
        cycle += 1
        check()
    else:
        _, delta = line.split(" ")
        delta = int(delta)
        cycle += 1
        check()
        cycle += 1
        check()
        x += delta

print(total)
