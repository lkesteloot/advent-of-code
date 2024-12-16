
import time
import numpy as np
import heapq

lines = open("input-16-test-1.txt").read().splitlines()
lines = open("input-16-test-2.txt").read().splitlines()
lines = open("input-16.txt").read().splitlines()

GRID = np.array([list(line) for line in lines])
START = tuple(np.argwhere(GRID == "S")[0])
END = tuple(np.argwhere(GRID == "E")[0])

NORTH = -1, 0
EAST = 0, 1
SOUTH = 1, 0
WEST = 0, -1

# Dijkstra's shortest path.
class Dijkstra:
    # start_node: node where we start to search.
    # end_nodes: set of nodes where to stop.
    # get_neighbors(node): get list of neighbors of node.
    # get_cost(node1, node2): get cost of going from node1 to node2.
    def __init__(self, start_node, end_nodes, get_neighbors, get_cost):
        self.start_node = start_node
        self.end_nodes = end_nodes
        self.get_neighbors = get_neighbors
        self.get_cost = get_cost
        self.h = []
        self.visited = set()
        self.distance = {}
        self.distance[start_node] = 0
        heapq.heappush(self.h, (0, start_node))
        # Map from node to list of previous nodes.
        self.back = {}

    # Returns (cost, path).
    def go(self):
        while True:
            while True:
                if not self.h:
                    return
                value, node = heapq.heappop(self.h)
                if node not in self.visited:
                    break

            neighbors = self.get_neighbors(node)
            node_dist = self.distance[node]
            for neighbor in neighbors:
                if not neighbor in self.visited:
                    cost = self.get_cost(node, neighbor)
                    neighbor_dist = self.distance.get(neighbor)
                    new_dist = node_dist + cost
                    if neighbor_dist == None or new_dist < neighbor_dist:
                        self.distance[neighbor] = new_dist
                        heapq.heappush(self.h, (new_dist, neighbor))
                        self.back[neighbor] = [node]
                    elif new_dist == neighbor_dist:
                        self.back[neighbor].append(node)

def add(p, d):
    return p[0] + d[0], p[1] + d[1]

def turn_right(d):
    return d[1], -d[0]

def turn_left(d):
    return -d[1], d[0]

def do_puzzle():
    def get_neighbors(node):
        p, d = node
        neighbors = [
                (p, turn_left(d)),
                (p, turn_right(d)),
        ]
        new_p = add(p, d)
        if GRID[new_p] != "#":
            neighbors.append( (new_p, d) )

        return neighbors

    def get_cost(node1, node2):
        p1, d1 = node1
        p2, d2 = node2
        if p1 == p2 and d1 != d2:
            return 1000
        else:
            return 1

    dij = Dijkstra((START, EAST), {(END, NORTH), (END, EAST), (END, SOUTH), (END, WEST)}, get_neighbors, get_cost)
    dij.go()

    best_distance = min(d for d in (dij.distance.get(node) for node in dij.end_nodes) if d is not None)

    tiles = set()
    to_do = set(node for node in dij.end_nodes if dij.distance.get(node) == best_distance)
    while to_do:
        node = to_do.pop()
        if node not in tiles:
            tiles.add(node[0])
            if node[0] != START:
                to_do.update(dij.back[node])

    return best_distance, len(tiles)

def main():
    before = time.perf_counter()
    part1, part2 = do_puzzle()
    after = time.perf_counter()
    elapsed = round((after - before)*1_000_000)
    unit = "µs"
    if elapsed >= 1000:
        elapsed //= 1000
        unit = "ms"
    print(f"Parts 1 and 2: {part1} {part2} ({elapsed:,} {unit})")

main()
