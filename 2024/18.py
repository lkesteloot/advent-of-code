
import time, heapq
from collections import defaultdict

lines = open("input-18-test.txt").read().splitlines(); MAX_COORD = 6; PART_1_STEPS = 12
lines = open("input-18.txt").read().splitlines(); MAX_COORD = 70; PART_1_STEPS = 1024

COORDS = [tuple(map(int, line.split(","))) for line in lines]

# Map from coordinate to timestamp when that coordinate was corrupted.
GOT_BAD_AT = {(x, y): t for t, (x, y) in enumerate(COORDS)}

DELTA = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def neighbors_of(node, steps):
    neighbors = []
    for dx, dy in DELTA:
        n = node[0] + dx, node[1] + dy
        if 0 <= n[0] <= MAX_COORD and 0 <= n[1] <= MAX_COORD and GOT_BAD_AT.get(n, 100000) >= steps:
            neighbors.append(n)
    return neighbors

def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current)
    return list(reversed(total_path))

def d(a, b):
    return 1

# A* finds a path from start to goal.
# h is the heuristic function. h(n) estimates the cost to reach goal from node n.
def a_star(start, goal, h, steps, want_path):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet = {start}

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from the start
    # to n currently known.
    cameFrom = {}

    # For node n, gScore[n] is the currently known cost of the cheapest path from start to n.
    gScore = defaultdict(lambda: 99999999999)
    gScore[start] = 0

    # For node n, fScore[n] = gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore = defaultdict(lambda: 99999999999)
    fScore[start] = h(start)

    while openSet:
        # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        current = min( (fScore[n], n) for n in openSet)[1]
        if current == goal:
            return reconstruct_path(cameFrom, current) if want_path else True

        openSet.remove(current)
        for neighbor in neighbors_of(current, steps):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore = gScore[current] + d(current, neighbor)
            if tentative_gScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + h(neighbor)
                if neighbor not in openSet:
                    openSet.add(neighbor)

    # Open set is empty but goal was never reached
    return None if want_path else False

def h(a, b):
    # Manhattan distance.
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def do_part(part):
    start = (0, 0)
    goal = (MAX_COORD, MAX_COORD)

    if part == 1:
        path = a_star(start, goal, lambda node: h(node, goal), PART_1_STEPS, True)
        return len(path) - 1
    else:
        lo = 0
        hi = len(COORDS)
        while lo < hi:
            mid = (lo + hi) // 2

            found_path = a_star(start, goal, lambda node: h(node, goal), mid, False)
            if found_path:
                lo = mid + 1
            else:
                hi = mid

        x, y = COORDS[hi - 1]
        return str(x) + "," + str(y)

def main():
    for part in [1, 2]:
        before = time.perf_counter()
        answer = do_part(part)
        after = time.perf_counter()
        elapsed = round((after - before)*1_000_000)
        unit = "µs"
        if elapsed >= 1000:
            elapsed //= 1000
            unit = "ms"
        print(f"Part {part}: {answer} ({elapsed:,} {unit})")

main()
