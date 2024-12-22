
import time, heapq
from itertools import *
from functools import *
import numpy as np

lines = open("input-21-test.txt").read().splitlines()
lines = open("input-21.txt").read().splitlines()

# Dijkstra's shortest path.
class Dijkstra:
    def __init__(self, start_node, end_node, get_neighbors):
        self.start_node = start_node
        self.end_node = end_node
        self.get_neighbors = get_neighbors
        self.left_to_visit = []
        self.visited_nodes = set()
        self.cost_to_start = {}
        self.cost_to_start[start_node] = 0
        heapq.heappush(self.left_to_visit, (0, start_node))

    # Returns cost.
    def go(self):
        while True:
            while True:
                if not self.left_to_visit:
                    raise Exception("no path to end node")

                value, node = heapq.heappop(self.left_to_visit)
                if node not in self.visited_nodes:
                    break

            if node == self.end_node:
                return self.cost_to_start[node]

            cost_to_us = self.cost_to_start[node]
            for neighbor, cost_from_us_to_neighbor in self.get_neighbors(node):
                if not neighbor in self.visited_nodes:
                    cost_to_neighbor = self.cost_to_start.get(neighbor)
                    cost_to_neighbor_through_us = cost_to_us + cost_from_us_to_neighbor
                    if cost_to_neighbor == None or cost_to_neighbor_through_us < cost_to_neighbor:
                        self.cost_to_start[neighbor] = cost_to_neighbor_through_us
                        heapq.heappush(self.left_to_visit, (cost_to_neighbor_through_us, neighbor))

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

# start and end are keys on current keypad. keypads_below are
# the number of keypads below it. assumes that all keypads
# below it start and end with all "A".
# returns number of keys pressed by human.
@cache
def find_best_keys_to_push_button(start, end, keypads_above, keypads_below):
    if keypads_below == 0 or start == end:
        # Can just press the key.
        return 1

    keypad_neighbors = NUMERIC_NEIGHBORS if keypads_above == 0 else DIRECTIONAL_NEIGHBORS

    def get_neighbors(state):
        neighbors = []
        our_key, sub_key = state

        # Figure out how to move.
        for d, new_our_key in enumerate(keypad_neighbors[our_key]):
            if new_our_key is not None:
                new_sub_key = DIRECTION_TO_KEY[d]
                cost = find_best_keys_to_push_button(sub_key, new_sub_key, keypads_above + 1, keypads_below - 1)
                neighbors.append( ((new_our_key, new_sub_key), cost) )

        # Also figure out how to press current key.
        new_sub_key = "A"
        cost = find_best_keys_to_push_button(sub_key, new_sub_key, keypads_above + 1, keypads_below - 1)
        neighbors.append( ((our_key, new_sub_key), cost) )

        return neighbors

    # State is key we're on and key that sub-keypad is on.
    d = Dijkstra((start, "A"), (end, "A"), get_neighbors)
    return d.go()

def do_part(part):
    directional_keypad_robot_count = 2 if part == 1 else 25

    total = 0
    for line in lines:
        cost = sum(find_best_keys_to_push_button(a, b, 0, directional_keypad_robot_count + 1)
                   for a, b in pairwise("A" + line))
        total += cost * int(line[:-1])
    return total

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
