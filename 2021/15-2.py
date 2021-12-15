
import dijkstra

lines = [line.strip() for line in open("input-15-test.txt")]

risks = [list(map(int, list(line))) for line in lines]
width = len(risks[0])
height = len(risks)

if True:
    risks = [
        [(risks[y % height][x % width] + (y // height) + (x // width) - 1) % 9 + 1 for x in range(width*5)]
        for y in range(height*5)
    ]
    width *= 5
    height *= 5

def get_neighbors(node):
    x, y = node
    n = []
    if x > 0: n.append((x - 1, y))
    if x < width - 1: n.append((x + 1, y))
    if y > 0: n.append((x, y - 1))
    if y < height - 1: n.append((x, y + 1))
    return n

def get_cost(node1, node2):
    x, y = node2
    return risks[y][x]

d = dijkstra.Dijkstra((0, 0), (width - 1, height - 1), 99999, get_neighbors, get_cost)
cost, path = d.go()
print(cost, path)
for y in range(height):
    parts = []
    for x in range(width):
        bold = (x, y) in path
        if bold:
            parts.append(chr(27) + "[1m")
        else:
            parts.append(chr(27) + "[2m")
        parts.append(str(risks[y][x]))
        parts.append(chr(27) + "[0m")
    print("".join(parts))

