
from itertools import combinations

lines = open("input-11.txt").read().splitlines()

expand = 1000000

width, height = len(lines[0]), len(lines)
galaxies = [(x, y) for y in range(height) for x in range(width) if lines[y][x] == "#"]

missing_x = set(range(width)) - set(x for x, y in galaxies)
missing_y = set(range(height)) - set(y for x, y in galaxies)

def adjust(x, missing):
    return x + sum(expand - 1 for v in missing if v < x)

def adjust_p(p):
    return adjust(p[0], missing_x), adjust(p[1], missing_y)

galaxies = [adjust_p(p) for p in galaxies]

total = sum(abs(g1[0] - g2[0]) + abs(g1[1] - g2[1]) for g1, g2 in combinations(galaxies, 2))

print(total)
