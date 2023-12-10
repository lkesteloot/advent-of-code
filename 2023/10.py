
lines = open("input-10.txt").read().splitlines()
width, height = len(lines[0]), len(lines)
tiles = {(x, y): lines[y][x] for y in range(height) for x in range(width)}

# Up, right, down, left.
DELTA = [(0,-1), (1,0), (0,1), (-1,0)]
TURNS = ["7|F", "J-7", "L|J", "F-L"]

def add(a,b):
    return a[0] + b[0], a[1] + b[1]

def on_board(p):
    return 0 <= p[0] < width and 0 <= p[1] < height

# Find start tile.
start_p = next(p for p, ch in tiles.items() if ch == "S")

# Find initial direction.
for i in range(4):
    np = add(start_p, DELTA[i])
    if on_board(np) and tiles[np] in TURNS[i]:
        start_d = i
        break
else:
    print("start not found")

# Find path.
path = set()
p = start_p
d = start_d
while True:
    path.add(p)
    p = add(p, DELTA[d])
    if p == start_p:
        break
    d = (d + TURNS[d].index(tiles[p]) - 1) % 4
end_d = d
print("steps", len(path)//2)

# Replace S.
tiles[start_p] = TURNS[end_d][(start_d - end_d + 1) % 4]

# Find inside tiles.
count = 0
started_with_F = None
for y in range(height):
    # Flip on every vertical transition.
    inside = False
    for x in range(width):
        p = x, y
        if p in path:
            ch = tiles[p]
            if ch == "F":
                started_with_F = True
            elif ch == "L":
                started_with_F = False
            elif ch == "|" or (ch == "J" if started_with_F else ch == "7"):
                inside = not inside
        elif inside:
            count += 1
    if inside:
        print("Ended inside", y)
print("inside", count)
