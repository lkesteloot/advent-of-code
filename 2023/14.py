
from collections import defaultdict
from itertools import chain
from more_itertools import pairwise

lines = open("input-14.txt").read().splitlines()

width = len(lines[0])
height = len(lines)

rolls = [(x, y) for y in range(height) for x in range(width) if lines[y][x] == "O"]
squares = [(x, y) for y in range(height) for x in range(width) if lines[y][x] == "#"]

# clockwise 90 degrees
def rotate():
    global rolls, squares
    rolls = [(width - 1 - y, x) for x, y in rolls]
    squares = [(width - 1 - y, x) for x, y in squares]

tile_to_y1 = {}
for d in range(4):
    for x in range(width):
        col_squares = chain(((x, -1),), sorted(p for p in squares if p[0] == x), ((x, height),))
        for p1, p2 in pairwise(col_squares):
            y1, y2 = p1[1] + 1, p2[1]
            for y in range(y1, y2):
                tile_to_y1[d, x, y] = y1
    rotate()

squares = [] # Don't need these anymore

def tilt(d):
    global rolls, tile_to_y1

    counts = defaultdict(int)
    new_rolls = []

    for x, y in rolls:
        y1 = tile_to_y1[d, x, y]
        key = x, y1
        new_rolls.append( (x, y1 + counts[key]) )
        counts[key] += 1

    rolls = new_rolls

def main():
    count = 0
    prev = {} # roll to count
    prevn = {} # count to roll
    while True:
        for d in range(4):
            tilt(d)
            rotate()
        count += 1
        rolls.sort()
        key = tuple(rolls)
        if key in prev:
            first = prev[key]
            ans_rolls = prevn[(1000000000 - first) % (count - first) + first]
            print(sum(height - p[1] for p in ans_rolls))
            break
        prev[key] = count
        prevn[count] = key
        #print(count, sum(height - p[1] for p in rolls))

main()
