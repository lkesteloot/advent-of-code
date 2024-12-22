
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

    # Returns (cost, path, end node).
    def go(self):
        while True:
            while True:
                if not self.left_to_visit:
                    raise Exception("no path to end node")

                value, node = heapq.heappop(self.left_to_visit)
                if node not in self.visited_nodes:
                    break

            if self.is_end_node(node):
                return self.cost_to_start[node], self._make_path(node), node

            cost_to_us = self.cost_to_start[node]
            for neighbor, keys_from_us_to_neighbor in self.get_neighbors(node):
                if not neighbor in self.visited_nodes:
                    cost_from_us_to_neighbor = len(keys_from_us_to_neighbor)
                    cost_to_neighbor = self.cost_to_start.get(neighbor)
                    cost_to_neighbor_through_us = cost_to_us + cost_from_us_to_neighbor
                    if cost_to_neighbor == None or cost_to_neighbor_through_us < cost_to_neighbor:
                        self.cost_to_start[neighbor] = cost_to_neighbor_through_us
                        heapq.heappush(self.left_to_visit, (cost_to_neighbor_through_us, neighbor))
                        self.back[neighbor] = node, keys_from_us_to_neighbor

    def _make_path(self, end_node):
        all_keys = []
        node = end_node
        while node != self.start_node:
            node, keys = self.back[node]
            all_keys.append(keys)
        return "".join(reversed(all_keys))

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

def tuple_with(t, i, v):
    return tuple(t[:i]) + (v,) + tuple(t[i + 1:])

def find_cost_of_code(target_code, directional_keypad_robot_count):
    # What we've typed so far, and location of robots.
    state = ("", "A") + ("A",)*directional_keypad_robot_count

    def get_neighbors(state):
        code, r1, *r = state

        neighbors = []

        # See if we can move last robot.
        i = len(r) - 1
        for d, r_neighbor in enumerate(DIRECTIONAL_NEIGHBORS[r[i]]):
            if r_neighbor is not None:
                neighbors.append( ((code, r1) + tuple_with(r, i, r_neighbor), DIRECTION_TO_KEY[d]) )

        # See if we can move middle robots.
        while i > 0:
            if r[i] != "A":
                r_neighbor = DIRECTIONAL_NEIGHBORS[r[i - 1]][KEY_TO_DIRECTION[r[i]]]
                if r_neighbor is not None:
                    neighbors.append( ((code, r1) + tuple_with(r, i - 1, r_neighbor), "A") )
                break
            i -= 1

        # See if we can move r1.
        if i == 0:
            if r[i] != "A":
                r_neighbor = NUMERIC_NEIGHBORS[r1][KEY_TO_DIRECTION[r[i]]]
                if r_neighbor is not None:
                    neighbors.append( ((code, r_neighbor) + tuple(r), "A") )
            else:
                # See if we can press a digit.
                new_code = code + r1
                if target_code.startswith(new_code):
                    neighbors.append( ((new_code, r1) + tuple(r), "A") )

        return neighbors

    d = Dijkstra(state,
                 lambda state: state[0] == target_code,
                 get_neighbors,
                 lambda a, b: 1)
    cost, (path, keys) = d.go()

    #print(target_code, cost, keys)
    print(target_code, cost)
    #print(path)

    return cost

# start and end are keys on current keypad. keypads_below are
# the number of keypads below it. assumes that all keypads
# below it start and end with all "A".
# returns sequence of lowest keys.
@cache
def find_best_keys_to_push_button(start, end, keypads_above, keypads_below):
    if keypads_below == 0:
        # Can just press the key.
        return end

    keypad_neighbors = NUMERIC_NEIGHBORS if keypads_above == 0 else DIRECTIONAL_NEIGHBORS

    def get_neighbors(state):
        our_key, sub_key = state
        neighbors = []
        for d, new_our_key in enumerate(keypad_neighbors[our_key]):
            if new_our_key is not None:
                new_sub_key = DIRECTION_TO_KEY[d]
                keys = find_best_keys_to_push_button(sub_key, new_sub_key, keypads_above + 1, keypads_below - 1)
                neighbors.append( ((new_our_key, new_sub_key), keys) )

        # Also figure out how to press current key.
        new_sub_key = "A"
        keys = find_best_keys_to_push_button(sub_key, new_sub_key, keypads_above + 1, keypads_below - 1)
        neighbors.append( ((our_key, new_sub_key), keys) )

        return neighbors

    # State is key we're on and key that sub-keypad is on.
    d = Dijkstra((start, "A"),
                 lambda state: state == (end, "A"),
                 get_neighbors,
                 None)
    cost, keys, end_state = d.go()
    if keys == "":
        keys = "A"
    #keys += "A" # find_best_keys_to_push_button(end_state[1], "A", keypads_above + 1, keypads_below - 1)
    #print("    "*keypads_above, cost, keys)
    return keys

def simulate(keys, keypads_above, numeric_start="A"):
    print("    ", keys)
    if keypads_above == 0:
        return
    sub_keys = ""
    pos = numeric_start if keypads_above == 1 else "A"
    keypad_neighbors = NUMERIC_NEIGHBORS if keypads_above == 1 else DIRECTIONAL_NEIGHBORS
    for key in keys:
        if key == ".":
            sub_keys += "."
        elif key == "A":
            sub_keys += pos
        else:
            d = KEY_TO_DIRECTION[key]
            pos = keypad_neighbors[pos][d]
            sub_keys += "."
    simulate(sub_keys, keypads_above - 1, numeric_start)

def do_part(part):
    directional_keypad_robot_count = 2 if part == 1 else 20

    total = 0
    for line in lines:
        all_keys = ""
        for a, b in pairwise("A" + line):
            keys = find_best_keys_to_push_button(a, b, 0, directional_keypad_robot_count + 1)
            all_keys += keys
        cost = len(all_keys)
        #simulate(all_keys, directional_keypad_robot_count + 1)
        #print(line, cost, all_keys)
        total += cost * int(line[:-1])
    return total

def main():
    if False:
        keys = find_best_keys_to_push_button("3", "3", 0, 1)
        print("3 to 3", keys)
        print("Good")
        simulate("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A", 3)
        print("Bad")
        simulate("v<<A>^>AvA^Av<<A>^>AAv<A<A>^>AAvAA^<A>Av<A^>AA<A>Av<A<A>^>AAA<Av>A^A", 3)
        print("Bad part")
        qq = 3
        keys = find_best_keys_to_push_button("3", "7", 0, qq)
        simulate(keys, qq, numeric_start="3")
        #return
        #keys = find_best_keys_to_push_button("A", "<", 3)
        #print(keys)
        #return
    # 126384, 176452
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

"""
029A 28 v<<A>^>A<A>A<AAv>A^Av<AAA^>A
r3   v<<A>^>A<A>A<AAv>A^Av<AAA^>A
r2  A>v<*v^A*^*A*^**v>*A*>v***^A*
r1  A   0   * 2 * 58  9 *  63A  *
out         0   2       9       *
"""


"""
correct:    <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
mine fixed: <v<A>>^AvA^Av<<A>^>AAv<A<A>^>AAvAA^<A>Av<A^>AA<A>Av<A<A>^>AAA<Av>A^A
mine:       v<<A>^>AvA^Av<<A>^>AAv<A<A>^>AAvAA^<A>Av<A^>AA<A>Av<A<A>^>AAA<Av>A^A
            v<<A>^>AvA^Av<<A>^>AAv<A<A>^>AAvAA^<A>Av<A^>AA<A>Av<A<A>^>AAA<Av>A^A
"""

