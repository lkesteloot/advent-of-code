
import heapq
from collections import defaultdict

part2 = True

lines = open("input-17.txt").read().splitlines()

width = len(lines[0])
height = len(lines)
tiles = {(x, y): int(lines[y][x]) for y in range(height) for x in range(width)}

def get_run(path):
    ds = "".join(d for _, d in path[-10:])
    d = ds[-1]
    run = len(ds) - len(ds.rstrip(d))
    return d, run

def neighbors(node, path):
    last_dir = path[-1][1]
    if last_dir in ".>":
        options = [
                ("^", (node[0], node[1] - 1)),
                ("v", (node[0], node[1] + 1)),
                (">", (node[0] + 1, node[1])),
        ]
    elif last_dir in ".<":
        options = [
                ("^", (node[0], node[1] - 1)),
                ("v", (node[0], node[1] + 1)),
                ("<", (node[0] - 1, node[1])),
        ]
    elif last_dir in ".v":
        options = [
                ("<", (node[0] - 1, node[1])),
                (">", (node[0] + 1, node[1])),
                ("v", (node[0], node[1] + 1)),
        ]
    elif last_dir in ".^":
        options = [
                ("<", (node[0] - 1, node[1])),
                (">", (node[0] + 1, node[1])),
                ("^", (node[0], node[1] - 1)),
        ]

    ch, run = get_run(path)
    must = None
    avoid = None
    if part2:
        if run < 4 and last_dir != ".":
            must = ch
        elif run >= 10:
            avoid = ch
    else:
        if run >= 3:
            avoid = ch

    for new_dir, new_node in options:
        if 0 <= new_node[0] < width and 0 <= new_node[1] < height and \
                new_dir != avoid and (must is None or new_dir == must):
            yield new_dir, new_node

def shortest_path(start, end):
    seen = set()
    queue = [(0, (start, [(start, ".")]))]
    while queue:
        cost, (node, path) = heapq.heappop(queue)
        lastn = "".join(d for _, d in path[-10 if part2 else -3:])
        key = (node, lastn)
        if key not in seen:
            seen.add(key)
            if node == end and (not part2 or get_run(path)[1] >= 4):
                return cost, path
            for new_dir, neighbor in neighbors(node, path):
                heapq.heappush(queue, (cost + tiles[neighbor],
                                       (neighbor, path + [(neighbor, new_dir)])))

cost, path = shortest_path((0, 0), (width - 1, height - 1))
for y in range(height):
    parts = []
    for x in range(width):
        p = (x, y)
        for node, dir in path:
            if node == p and dir != ".":
                parts.append(dir)
                break
        else:
            parts.append(str(tiles[p]))
    print("".join(parts))
print(cost)

