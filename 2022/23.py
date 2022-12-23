
from collections import defaultdict

lines = [line.strip() for line in open("input-23-test.txt")]
lines = [line.strip() for line in open("input-23.txt")]

elves = set()  # (x,y)

y = 0
for line in lines:
    for x in range(len(line)):
        if line[x] == "#":
            elves.add((x, y))
    y += 1

def get_bounds(elves):
    x1, y1 = 10000, 10000
    x2, y2 = -10000, -10000

    for x, y in elves:
        x1 = min(x1, x)
        y1 = min(y1, y)
        x2 = max(x2, x)
        y2 = max(y2, y)

    return x1, y1, x2, y2

def print_elves(elves):
    x1, y1, x2, y2 = get_bounds(elves)

    for y in range(y1, y2 + 1):
        s = ""
        for x in range(x1, x2 + 1):
            if (x, y) in elves:
                s += "#"
            else:
                s += "."
        print(s)

# print_elves(elves)

counter = 0
for rnd in range(10000):
    print(rnd)
    # proposed pos to orig pos
    proposed = defaultdict(lambda: [])

    any_move = False
    for x, y in elves:
        nw = (x - 1, y - 1) not in elves
        n = (x, y - 1) not in elves
        ne = (x + 1, y - 1) not in elves
        w = (x - 1, y) not in elves
        sw = (x - 1, y + 1) not in elves
        s = (x, y + 1) not in elves
        se = (x + 1, y + 1) not in elves
        e = (x + 1, y) not in elves

        above = nw and n and ne
        below = sw and s and se
        left = nw and w and sw
        right = ne and e and se

        around = above and below and left and right

        if around:
            proposed[(x, y)].append((x, y))
        else:
            options = [
                    (nw, n, ne, x, y - 1),
                    (sw, s, se, x, y + 1),
                    (nw, w, sw, x - 1, y),
                    (ne, e, se, x + 1, y),
            ]
            for i in range(4):
                ii = (counter + i) % 4
                d1, d2, d3, nx, ny = options[ii]
                if d1 and d2 and d3:
                    proposed[(nx, ny)].append((x, y))
                    any_move = True
                    break
            else:
                proposed[(x, y)].append((x, y))

    new_elves = set()
    for p, from_list in proposed.items():
        if len(from_list) == 1:
            new_elves.add(p)
        else:
            for from_p in from_list:
                new_elves.add(from_p)

    elves = new_elves

    counter += 1
    if not any_move:
        print("answer", rnd + 1)
        break

x1, y1, x2, y2 = get_bounds(elves)
print(x1, y1, x2, y2)

blank = (x2 - x1 + 1)*(y2 - y1 + 1) - len(elves)
print(blank)

