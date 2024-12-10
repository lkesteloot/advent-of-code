
# mv ~/Downloads/input.txt input-xx.txt

import sys, re, time
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
import numpy as np
# import scipy.signal

lines = open("input-xx-test.txt").read().splitlines()
#lines = open("input-xx.txt").read().splitlines()
# width = len(lines[0])
# height = len(lines)
# matrix = [list(map(int, list(line))) for line in lines]
# name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
# grid = np.array([list(line) for line in lines])
# yxs = (yx for yx, ch in np.ndenumerate(grid) if is_symbol(ch))
# tiles = {(x, y): lines[y][x] for y in range(height) for x in range(width)}
# rolls = {(x, y) for y in range(height) for x in range(width) if lines[y][x] == "O"}
#    for m in re.finditer(r"[0-9]+", line):
#        begin, end = m.span()
#        value = int(m.group(0))

def do_part(part):
    total = 0
    for line_number, line in enumerate(lines):
    for line in lines:
    return total

def main():
    for part in [1]:
        before = time.time()
        answer = do_part(part)
        after = time.time()
        elapsed = round((after - before)*1000000)
        unit = "µs"
        if elapsed >= 1000:
            elapsed //= 1000
            unit = "ms"
        print(f"Part {part}: {answer} ({elapsed:,} {unit})")

main()
