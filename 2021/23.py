
from heapq import *

COSTS = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
}

RIGHT_X = {
        "A": 3,
        "B": 5,
        "C": 7,
        "D": 9,
        ".": None,
}

HALLWAY_X = [1, 2, 4, 6, 8, 10, 11]

lines = [line[:-1] for line in open("input-23.txt")]

MAX_Y = len(lines) - 1

h = []
unique = set()

def push(cost, lines):
    x = (cost, tuple(lines))
    if x not in unique:
        unique.add(x)
        heappush(h, x)

def pop():
    x = heappop(h)
    unique.remove(x)
    cost, t = x
    return cost, list(t)

def print_lines(cost, lines):
    print(cost)
    for line in lines:
        print(line)
    print()

def move(lines, x1, y1, x2, y2):
    lines = [list(line) for line in lines]
    ch = lines[y1][x1]
    if y2 > 1:
        ch = ch.lower()
    lines[y2][x2] = ch
    lines[y1][x1] = "."
    lines = ["".join(line) for line in lines]
    return lines

def generate_moves(cost, lines, x, y):
    orig_x = x
    orig_y = y

    ch = lines[y][x]
    c = COSTS[ch]
    #print("Generating moves for", x, y, ch)

    if y == 1:
        # Hallway. Must go to room.
        t = RIGHT_X[ch]
        for yy in range(2, MAX_Y):
            if lines[yy][t] != "." and lines[yy][t].lower() != ch.lower():
                # Room has wrong person in it.
                return
        # Can move to this room.
        while t < x and lines[y][x - 1] == ".":
            x -= 1
            cost += c
        while t > x and lines[y][x + 1] == ".":
            x += 1
            cost += c
        if t == x:
            while lines[y + 1][x] == '.':
                y += 1
                cost += c
            push(cost, move(lines, orig_x, orig_y, x, y))
    else:
        for yy in range(2, y):
            if lines[yy][x] != ".":
                # Blocked.
                return
        if RIGHT_X[ch] == x:
            for yy in range(y + 1, MAX_Y):
                if lines[yy][x].upper() != ch:
                    # Wrong person below us.
                    break
            else:
                # Everyone good below us.
                return

        while y > 1:
            y -= 1
            cost += c
        for t in HALLWAY_X:
            new_cost = cost
            x = orig_x
            while t < x and lines[y][x - 1] == ".":
                x -= 1
                new_cost += c
            while t > x and lines[y][x + 1] == ".":
                x += 1
                new_cost += c
            if t == x:
                push(new_cost, move(lines, orig_x, orig_y, x, y))

def all_good(lines):
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            ch = line[x].upper()
            if ch in COSTS and RIGHT_X[ch] != x:
                return False

    return True

push(0, lines)

while True:
    cost, lines = pop()
    # print("Heap size:", len(h), "cost:", cost)
    # print_lines(cost, lines)
    if all_good(lines):
        print_lines(cost, lines)
        break
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            if line[x] in COSTS:
                generate_moves(cost, lines, x, y)

