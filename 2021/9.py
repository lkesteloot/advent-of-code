
lines = list(line.strip() for line in open("input-9.txt"))
width = len(lines[0])
height = len(lines)

low_points = []

for y in range(height):
    for x in range(width):
        h = lines[y][x]
        if not (x > 0 and h >= lines[y][x - 1]) and \
            not (x < width - 1 and h >= lines[y][x + 1]) and \
            not (y > 0 and h >= lines[y - 1][x]) and \
            not (y < height - 1 and h >= lines[y + 1][x]):

            low_points.append( (x, y) )

def f(used, x, y):
    if x < 0 or y < 0 or x >= width or y >= height or used[y][x] or lines[y][x] == '9':
        return 0

    used[y][x] = True

    return f(used, x - 1, y) + f(used, x + 1, y) + f(used, x, y - 1) + f(used, x, y + 1) + 1

def flood_fill(x, y):
    used = []
    for i in range(height):
        used.append([False]*width)

    return f(used, x, y)

basins = []
for x, y in low_points:
    size = flood_fill(x, y)
    basins.append(size)

basins.sort()
total = 1
for size in basins[-3:]:
    total *= size

print(total)

