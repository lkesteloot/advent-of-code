
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

total = sum(abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])
    for i in range(len(galaxies) - 1) for j in range(i + 1, len(galaxies)))

print(total)

