
from collections import defaultdict
from itertools import *
import numpy as np

lines = open("input-8-test.txt").read().splitlines()
lines = open("input-8.txt").read().splitlines()

grid = np.array([list(line) for line in lines])
begin = np.array([0, 0])
end = np.array(grid.shape)

antennas = defaultdict(lambda: [])
for index, value in np.ndenumerate(grid):
    if value != ".":
        antennas[value].append(np.array(index))

def is_inside(p):
    return np.all((begin <= p) & (p < end))

def do_part(part):
    all_pos = []
    for letter, indexes in antennas.items():
        for i1, i2 in combinations(indexes, 2):
            d = i2 - i1

            if part == 1:
                all_pos.extend(filter(is_inside, [i1 - d, i2 + d]))
            else:
                p = i1
                while is_inside(p):
                    all_pos.append(p)
                    p = p + d
                p = i1
                while is_inside(p):
                    all_pos.append(p)
                    p = p - d

    print(f"Part {part}: {len(set(map(tuple, all_pos)))}")

do_part(1)
do_part(2)
