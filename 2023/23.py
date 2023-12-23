
from collections import defaultdict

lines = open("input-23.txt").read().splitlines()

part2 = True

DIRS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
SLOPES = "<^>v"

width = len(lines[0])
height = len(lines)

start = (1, 0)
end = (width - 2, height - 1)

# (sx,sy) -> [((dx,dy),dist), ...]
graph = defaultdict(list)
handled = set()

# Convert maze to graph.
def explore(op, p):
    global graph, width, height, handled

    if (op, p) in handled:
        return
    handled.add( (op, p) )

    dist = 0
    via = p
    last_p = op
    while True:
        dist += 1

        # Find all valid neighbors.
        new_points = []
        for dr, np in enumerate((p[0] + dx, p[1] + dy) for dx, dy in DIRS):
            if 0 <= np[0] < width and 0 <= np[1] < height and np != last_p:
                ch = lines[np[1]][np[0]]
                i = -1 if part2 else SLOPES.find(ch)
                if ch != "#" and (i < 0 or i == dr):
                    new_points.append(np)

        assert len(new_points) > 0 or p == start or p == end

        if len(new_points) == 1:
            # If only one, it's part of the same edge, keep going.
            last_p = p
            p = new_points[0]
        else:
            # End of edge, record it and start exploring new edges.
            graph[op].append( (p,dist) )
            print("can get from", op, "via", via, "to", p, "in", dist, "steps")
            for np in new_points:
                explore(p, np)
            break

explore(start, (start[0], start[1] + 1))

# Explore all possible paths from the start, keep track of the longest.
best_dist = 0
def extend_path(path, path_set, dist):
    global best_dist
    if path[-1] == end:
        if dist > best_dist:
            print("found path with length", dist)
            best_dist = dist
        return dist
    max_dist = 0
    for new_p, ddist in graph[path[-1]]:
        if new_p not in path_set:
            path_set.add(new_p)
            new_dist = extend_path(path + [new_p], path_set, dist + ddist)
            path_set.remove(new_p)
            max_dist = max(max_dist, new_dist)
    return max_dist

max_dist = extend_path([start], {start}, 0)
print("max_dist", max_dist)
