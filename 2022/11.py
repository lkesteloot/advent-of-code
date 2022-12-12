

# mv ~/Downloads/input.txt input-11.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-11-test.txt")]
lines = [line.strip() for line in open("input-11.txt")]
# matrix = [list(map(int, list(line))) for line in lines]

class Monkey:
    def __init__(self, items, op, divisible_by, if_true, if_false):
        self.items = items
        self.op = op
        self.divisible_by = divisible_by
        self.if_true = if_true
        self.if_false = if_false
        self.inspected = 0

    def __repr__(self):
        return "Monkey(%s,%s,%s,%s,%s)" % (self.items, self.op, self.divisible_by, self.if_true, self.if_false)

prod = 1
monkeys = []
for i in range(len(lines) // 7):
    s = lines[i*7 + 1]
    s = s[s.index(":") + 2:]
    items = list(map(int, s.split(", ")))

    s = lines[i*7 + 2]
    s = s[s.index("new = ") + 6:]
    op = s

    s = lines[i*7 + 3].split(" ")
    divisible_by = int(s[-1])
    prod *= divisible_by

    s = lines[i*7 + 4].split(" ")
    if_true = int(s[-1])

    s = lines[i*7 + 5].split(" ")
    if_false = int(s[-1])

    monkeys.append(Monkey(items, op, divisible_by, if_true, if_false))

for round in range(10000):
    for m in monkeys:
        while m.items:
            m.inspected += 1
            w = m.items.pop(0)
            p = m.op.split(" ")
            op1 = w
            if p[2] == "old":
                op2 = w
            else:
                op2 = int(p[2])
            if p[1] == "+":
                w = op1 + op2
            else:
                w = op1 * op2
            #w = w // 3
            w %= prod
            if w % m.divisible_by == 0:
                monkeys[m.if_true].items.append(w)
            else:
                monkeys[m.if_false].items.append(w)
    for m in monkeys:
        print(m.inspected, m.items)
    print()


i = sorted(m.inspected for m in monkeys)
print(i[-2]*i[-1])
