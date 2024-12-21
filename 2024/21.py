
# mv ~/Downloads/input.txt input-21.txt

import sys, re, time, heapq
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
import numpy as np
# import scipy.signal

lines = open("input-21-test.txt").read().splitlines()
lines = open("input-21.txt").read().splitlines()
# width = len(lines[0])
# height = len(lines)
# matrix = [list(map(int, list(line))) for line in lines]
# name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
# grid = np.array([list(line) for line in lines])
# grid = np.pad(grid, 1, constant_values=-1)
# yxs = (yx for yx, ch in np.ndenumerate(grid) if is_symbol(ch))
# tiles = {(x, y): lines[y][x] for y in range(height) for x in range(width)}
# rolls = {(x, y) for y in range(height) for x in range(width) if lines[y][x] == "O"}
#    for m in re.finditer(r"[0-9]+", line):
#        begin, end = m.span()
#        value = int(m.group(0))

# Dijkstra's shortest path.
class Dijkstra:
    # start_node: node where we start to search.
    # is_end_node: whether a node is an end node.
    # get_neighbors(node): get list of neighbors of node.
    # get_cost(node1, node2): get cost of going from node1 to node2.
    def __init__(self, start_node, is_end_node, get_neighbors, get_cost):
        self.start_node = start_node
        self.is_end_node = is_end_node
        self.get_neighbors = get_neighbors
        self.get_cost = get_cost
        self.left_to_visit = []
        self.visited_nodes = set()
        self.cost_to_start = {}
        self.cost_to_start[start_node] = 0
        heapq.heappush(self.left_to_visit, (0, start_node))
        # Map from node to list of previous nodes.
        self.back = {}

    # Returns (cost, path).
    def go(self):
        while True:
            while True:
                if not self.left_to_visit:
                    raise Exception("no path to target")

                value, node = heapq.heappop(self.left_to_visit)
                if node not in self.visited_nodes:
                    break

            if self.is_end_node(node):
                return (self.cost_to_start[node], self._make_path(node))

            neighbors = self.get_neighbors(node)
            cost_to_us = self.cost_to_start[node]
            for neighbor, r4_key in neighbors:
                if not neighbor in self.visited_nodes:
                    cost_from_us_to_neighbor = self.get_cost(node, neighbor)
                    cost_to_neighbor = self.cost_to_start.get(neighbor)
                    cost_to_neighbor_through_us = cost_to_us + cost_from_us_to_neighbor
                    if cost_to_neighbor == None or cost_to_neighbor_through_us < cost_to_neighbor:
                        self.cost_to_start[neighbor] = cost_to_neighbor_through_us
                        heapq.heappush(self.left_to_visit, (cost_to_neighbor_through_us, neighbor))
                        self.back[neighbor] = node, r4_key

    def _make_path(self, end_node):
        path = []
        keys = []
        node = end_node
        path.append(node)
        while node != self.start_node:
            node, r4_key = self.back[node]
            path.append(node)
            keys.append(r4_key)
        path.reverse()
        return path, "".join(reversed(keys))

DIRECTION_TO_KEY = ["^", ">", "v", "<"]
KEY_TO_DIRECTION = dict((key, d) for d, key in enumerate(DIRECTION_TO_KEY))

NUMERIC_NEIGHBORS = {
    "7": [None, "8", "4", None],
    "8": [None, "9", "5", "7"],
    "9": [None, None, "6", "8"],
    "4": ["7", "5", "1", None],
    "5": ["8", "6", "2", "4"],
    "6": ["9", None, "3", "5"],
    "1": ["4", "2", None, None],
    "2": ["5", "3", "0", "1"],
    "3": ["6", None, "A", "2"],
    "0": ["2", "A", None, None],
    "A": ["3", None, None, "0"],
}

DIRECTIONAL_NEIGHBORS = {
    "<": [None, "v", None, None],
    "v": ["^", ">", None, "<"],
    ">": ["A", None, None, "v"],
    "^": [None, "A", "v", None],
    "A": [None, None, ">", "^"],
}

def find_cost_of_code(target_code, directional_keypad_robot_count):
    # What we've typed so far, and location of robots.
    state = ("", "A") + ("A",)*directional_keypad_robot_count

    def get_neighbors(state):
        code, r1, *r = state
        r2, r3 = r

        neighbors = []

        # See if we can move r3.
        for d, r3_neighbor in enumerate(DIRECTIONAL_NEIGHBORS[r3]):
            if r3_neighbor is not None:
                neighbors.append( ((code, r1, r2, r3_neighbor), DIRECTION_TO_KEY[d]) )

        # See if we can move r2.
        if r3 != "A":
            r2_neighbor = DIRECTIONAL_NEIGHBORS[r2][KEY_TO_DIRECTION[r3]]
            if r2_neighbor is not None:
                neighbors.append( ((code, r1, r2_neighbor, r3), "A") )
        else:
            # See if we can move r1.
            if r2 != "A":
                r1_neighbor = NUMERIC_NEIGHBORS[r1][KEY_TO_DIRECTION[r2]]
                if r1_neighbor is not None:
                    neighbors.append( ((code, r1_neighbor, r2, r3), "A") )
            else:
                # See if we can press a digit.
                new_code = code + r1
                if target_code.startswith(new_code):
                    neighbors.append( ((new_code, r1, r2, r3), "A") )

        return neighbors

    d = Dijkstra(state,
                 lambda state: state[0] == target_code,
                 get_neighbors,
                 lambda a, b: 1)
    cost, (path, keys) = d.go()

    print(target_code, cost, keys)
    #print(path)

    return cost

def do_part(part):
    total = 0
    for line in lines:
        cost = find_cost_of_code(line, 2 if part == 1 else 3)
        total += cost * int(line[:-1])
    return total

def main():
    for part in [1]:
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
