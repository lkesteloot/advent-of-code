
lines = open("input-14.txt").read().splitlines()

width = len(lines[0])
height = len(lines)

rolls = {(x, y) for y in range(height) for x in range(width) if lines[y][x] == "O"}
squares = {(x, y): lines[y][x] for y in range(height) for x in range(width) if lines[y][x] == "#"}

def tilt(d):
    global rolls, squares, width, height
    while True:
        changed = False
        if d == 0:
            ps = sorted(rolls, key=lambda p: p[1])
            for p in ps:
                np = p[0], p[1] - 1
                if p[1] > 0 and np not in rolls and np not in squares:
                    rolls.remove(p)
                    rolls.add(np)
                    changed = True
        elif d == 1:
            ps = sorted(rolls)
            for p in ps:
                np = p[0] - 1, p[1]
                if p[0] > 0 and np not in rolls and np not in squares:
                    rolls.remove(p)
                    rolls.add(np)
                    changed = True
        elif d == 2:
            ps = sorted(rolls, key=lambda p: -p[1])
            for p in ps:
                np = p[0], p[1] + 1
                if p[1] < height - 1 and np not in rolls and np not in squares:
                    rolls.remove(p)
                    rolls.add(np)
                    changed = True
        elif d == 3:
            ps = sorted(rolls, key=lambda p: -p[0])
            for p in ps:
                np = p[0] + 1, p[1]
                if p[0] < width - 1 and np not in rolls and np not in squares:
                    rolls.remove(p)
                    rolls.add(np)
                    changed = True
        if not changed:
            break

def pprint():
    global rolls, squares, width, height
    for y in range(height):
        line = ""
        for x in range(width):
            p = (x, y)
            if p in rolls:
                ch = "O"
            elif p in squares:
                ch = "#"
            else:
                ch = "."
            line += ch
        print(line)
    print()

count = 0
prev = {} # roll to count
prevn = {} # count to roll
while True:
    tilt(0)
    tilt(1)
    tilt(2)
    tilt(3)
    #pprint()
    count += 1
    key = tuple(sorted(rolls))
    if key in prev:
        first = prev[key]
        ans_rolls = prevn[(1000000000 - first) % (count - first) + first]
        print(sum(height - p[1] for p in ans_rolls))
        break
    prev[key] = count
    prevn[count] = key
    #print(count, sum(height - p[1] for p in rolls))

