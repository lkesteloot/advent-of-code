
# mv ~/Downloads/input.txt input-18.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-18.txt")]
# matrix = [list(map(int, list(line))) for line in lines]

class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        if self.right is None:
            return str(self.left)
        else:
            return "[" + str(self.left) + "," + str(self.right) + "]"

s = ""
def parse():
    global s
    if s[0] == "[":
        s = s[1:]
        left = parse()
        if s[0] != ",":
            raise Exception("missing comma")
        s = s[1:]
        right = parse()
        if s[0] != "]":
            raise Exception("missing comma")
        s = s[1:]
        return Node(left, right)
    else:
        n = ""
        while s != "" and s[0] >= "0" and s[0] <= "9":
            n += s[0]
            s = s[1:]
        return Node(int(n), None)

already_exploded = False
right_value = None
left_node = None
def find_explode(n, depth):
    global already_exploded, right_value, left_node

    if n.right is not None:
        if depth >= 4 and not already_exploded:
            if n.left.right is not None:
                raise Exception("n.left is not a number: " + str(n))
            if n.right.right is not None:
                raise Exception("n.right is not a number: " + str(n))
            # print("    Exploding", n)
            right_value = n.right.left
            if left_node is not None:
                # print(type(left_node.left), type(n.left.left))
                left_node.left += n.left.left
                left_node = None
            already_exploded = True
            return Node(0, None)

        left = find_explode(n.left, depth + 1)
        right = find_explode(n.right, depth + 1)

        return Node(left, right)
    else:
        val = n.left
        if right_value is not None:
            val += right_value
            right_value = None
        n = Node(val, None)
        left_node = n
        return n

already_split = False
def find_split(n):
    global already_split
    if n.right is not None:
        return Node(find_split(n.left), find_split(n.right))
    else:
        if n.left >= 10 and not already_split:
            # print("    Splitting", n.left)
            already_split = True
            return Node(Node(n.left // 2, None), Node((n.left + 1) // 2, None))
        else:
            return n

def reduce(n):
    global already_exploded, right_value, already_split, left_node
    # print("Reducing: " + str(n))
    while True:
        already_exploded = False
        right_value = None
        left_node = None
        n = find_explode(n, 0)
        if already_exploded:
            # print("After explode: " + str(n))
            continue
        already_split = False
        n = find_split(n)
        if already_split:
            # print("After split: " + str(n))
            pass
        if not already_exploded and not already_split:
            return n

def add(a, b):
    print()
    print("adding", a, b)
    n = Node(a, b)
    n = reduce(n)
    return n

def mag(n):
    if n.right is None:
        return n.left
    else:
        return 3*mag(n.left) + 2*mag(n.right)

s = "[[[[[9,8],1],2],3],4]"
s = "[7,[6,[5,[4,[3,2]]]]]"
s = "[[6,[5,[4,[3,2]]]],1]"
s = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"
s = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"

if False:
    s = lines[0]
    n = parse()
    for line in lines[1:]:
        s = line
        n2 = parse()
        n = add(n, n2)

    print(n)
    print(mag(n))

max_mag = 0
for i in range(len(lines) - 1):
    s = lines[i]
    n1 = parse()

    for j in range(i + 1, len(lines)):
        s = lines[j]
        n2 = parse()

        m = mag(add(n1, n2))
        max_mag = max(max_mag, m)

        m = mag(add(n2, n1))
        max_mag = max(max_mag, m)
print(max_mag)
