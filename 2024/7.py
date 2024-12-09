
from itertools import *
from functools import *

lines = open("input-7-test.txt").read().splitlines()
lines = open("input-7.txt").read().splitlines()

def compute(a, op, b):
    if op == "+":
        return a + b
    if op == "*":
        return a * b
    if op == "||":
        return int(str(a) + str(b))
    raise Exception()

def compute_all(values, ops):
    return reduce(lambda a, b: (compute(a[0], b[1], b[0]), "?"),
                  zip(values, ["?"] + list(ops)))

def do_part(part):
    OPS = ["+", "*"]
    if part == 2:
        OPS.append("||")

    total = 0

    for line in lines:
        solution, rest = line.split(": ")
        solution = int(solution)

        values = list(map(int, rest.split(" ")))

        for ops in product(*[OPS]*(len(values) - 1)):
            result = compute_all(values, ops)[0]
            if result == solution:
                total += result
                break

    print(f"Part {part}: {total}")

do_part(1)
do_part(2)
