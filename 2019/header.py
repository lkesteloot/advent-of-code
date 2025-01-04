
# mv ~/Downloads/input.txt input-xx.txt

import sys, re, time
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
import numpy as np
# import scipy.signal
from intcode import run, run_with_io, parse_mem

data = open("input-xx-test.txt").read()
#data = open("input-xx.txt").read()
# width = len(lines[0])
# height = len(lines)
# matrix = [list(map(int, list(line))) for line in lines]
# name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
# grid = np.array([list(line) for line in lines])
# grid = np.pad(grid, 1, constant_values=-1)
# yxs = (yx for yx, ch in np.ndenumerate(grid) if is_symbol(ch))
# tiles = {(x, y): lines[y][x] for y in range(height) for x in range(width)}
# rolls = {(x, y) for y in range(height) for x in range(width) if lines[y][x] == "O"}
#    for m in re.finditer(r"[0-9]+", line):
#        begin, end = m.span()
#        value = int(m.group(0))

MEM = parse_mem(data)

def add(p, d):
    return p[0] + d[0], p[1] + d[1]

def print_grid(grid):
    for row in grid:
        print("".join(str(tile) for tile in row))

def do_part(part):
    total = 0
    for line_number, line in enumerate(lines):
    for line in lines:
    return total

def main():
    for part in [1]:
        before = time.perf_counter()
        answer = do_part(part)
        after = time.perf_counter()
        elapsed = round((after - before)*1_000_000)
        unit = "µs"
        if elapsed >= 1000:
            elapsed //= 1000
            unit = "ms"
        print(f"Part {part}: {answer} ({elapsed:,} {unit})")

main()
