
lines = open("input-16.txt").read().splitlines()

width = len(lines[0])
height = len(lines)

# CSS directions
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

most_energy = 0
def go(p):
    global most_energy

    seen = set()
    energized = set()

    # (x, y, dir)
    lights = [p]
    while lights:
        light = lights.pop()
        if light in seen:
            continue
        seen.add(light)

        x, y, d = light
        dx, dy = DIRS[d]
        x, y = x + dx, y + dy
        if 0 <= x < width and 0 <= y < height:
            energized.add( (x, y) )
            ch = lines[y][x]
            if ch == "/":
                d = [1, 0, 3, 2][d]
                lights.append( (x, y, d) )
            elif ch == "\\":
                d = 3 - d
                lights.append( (x, y, d) )
            elif ch == "|":
                if d == 1 or d == 3:
                    lights.append( (x, y, 0) )
                    lights.append( (x, y, 2) )
                else:
                    lights.append( (x, y, d) )
            elif ch == "-":
                if d == 0 or d == 2:
                    lights.append( (x, y, 1) )
                    lights.append( (x, y, 3) )
                else:
                    lights.append( (x, y, d) )
            elif ch == ".":
                lights.append( (x, y, d) )

    most_energy = max(most_energy, len(energized))

for x in range(width):
    go( (x, -1, 2) )
    go( (x, height, 0) )
for y in range(height):
    go( (-1, y, 1) )
    go( (width, y, 3) )
print(most_energy)
