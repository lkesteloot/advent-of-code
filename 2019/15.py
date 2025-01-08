
import time, heapq
from collections import defaultdict
from intcode import Intcode, parse_mem

data = open("input-15.txt").read()
MEM = parse_mem(data)

DIRS = [
    None,
    (0,-1),     # North.
    (0,1),      # South.
    (-1,0),     # West.
    (1,0),      # East.
]

# Manhattan distance.
def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def sub(a, b):
    return a[0] - b[0], a[1] - b[1]

def neighbors_of(p):
    return set(add(p, d) for d in DIRS[1:])

# A* finds a path from start to goal.
# h is the heuristic function. h(n) estimates the cost to reach goal from node n.
# weight is actual distance between two nodes.
def a_star(start, goal, h, weight, neighbors_of, want_path):
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

    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet = []
    heapq.heappush(openSet, (fScore[start], start))

    processed = set()

    def reconstruct_path(current):
        total_path = [current]
        while current in cameFrom:
            current = cameFrom[current]
            total_path.append(current)
        return list(reversed(total_path))

    while openSet:
        _, current = heapq.heappop(openSet)
        if current == goal:
            return reconstruct_path(current) if want_path else True

        if current in processed:
            continue
        processed.add(current)

        for neighbor in neighbors_of(current):
            # weight(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore = gScore[current] + weight(current, neighbor)
            if tentative_gScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + h(neighbor)
                heapq.heappush(openSet, (fScore[neighbor], neighbor))

    # Open set is empty but goal was never reached
    return None if want_path else False

class RepairDroid(Intcode):
    def __init__(self, mem):
        super().__init__(mem)
        self.pos = 0,0
        # Map from (x,y) to whether there's a wall (boolean).
        self.is_wall = {self.pos: False}
        # Points to search.
        self.to_search = set()
        self.add_to_search()
        self.dir_sent = None
        self.oxygen_system = None
        self.directions = None

    def add_to_search(self):
        self.to_search |= neighbors_of(self.pos) - self.is_wall.keys()

    def get_path(self, p1, p2):
        return a_star(p1, p2, lambda p: dist(p, p2),
                      lambda a, b: 1, self.valid_neighbors_of, True)

    def input(self):
        if self.directions:
            self.dir_sent = self.directions.pop(0)
            return self.dir_sent

        assert self.to_search
        _, best = sorted((dist(p, self.pos),p) for p in self.to_search)[0]
        path = self.get_path(self.pos, best)
        self.directions = [DIRS.index(sub(path[i + 1], path[i]))  for i in range(len(path) - 1)]
        self.dir_sent = self.directions.pop(0)
        return self.dir_sent

    def output(self, v):
        dest = add(self.pos, DIRS[self.dir_sent])
        self.to_search -= {dest}
        if v == 0:
            # Hit a wall.
            self.is_wall[dest] = True
            # Must re-route.
            self.directions = None
        else:
            self.is_wall[dest] = False
            self.pos = dest
            self.add_to_search()
            if v == 2:
                self.oxygen_system = dest

    def valid_neighbors_of(self, p):
        return {p for p in neighbors_of(p) if not self.is_wall.get(p, False)}

    def print(self, path=set()):
        print("-"*50)
        min_x = min(x for x,_ in self.is_wall)
        min_y = min(y for _,y in self.is_wall)
        max_x = max(x for x,_ in self.is_wall)
        max_y = max(y for _,y in self.is_wall)
        for y in range(min_y, max_y + 1):
            print("".join("O" if (x,y) in path else ".#?"[self.is_wall.get((x,y), 2)]
                          for x in range(min_x, max_x + 1)))

droid = RepairDroid(MEM)

def do_part(part):
    global droid

    if part == 1:
        while not droid.halted and droid.to_search:
            droid.step()
        path = droid.get_path((0,0), droid.oxygen_system)
        return len(path) - 1
    else:
        has_oxygen = {droid.oxygen_system}
        walls = set(p for p in droid.is_wall.keys() if droid.is_wall[p])
        minutes = 0
        while True:
            new_has_oxygen = (set().union(*(neighbors_of(p) for p in has_oxygen)) | has_oxygen) - walls
            if has_oxygen == new_has_oxygen:
                break
            minutes += 1
            has_oxygen = new_has_oxygen
        return minutes

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
