
# mv ~/Downloads/input.txt input-25.txt

import sys, re
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-25-test.txt")]
lines = [line.strip() for line in open("input-25.txt")]
# matrix = [list(map(int, list(line))) for line in lines]
# name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)

DIGITS = {
        "2": 2,
        "1": 1,
        "0": 0,
        "-": -1,
        "=": -2,
}

RDIGITS = {
        -2: "=",
        -1: "-",
        0: "0",
        1: "1",
        2: "2",
}

def from_snafu(line):
    value = 0
    for ch in line:
        value = value*5 + DIGITS[ch]
    return value

def to_snafu(value):
    if value == 0:
        return "0"

    print(value)

    p = []
    carry = 0
    while value != 0:
        v = value % 5 + carry
        if v == 3:
            v = -2
            carry = 1
        elif v == 4:
            v = -1
            carry = 1
        elif v == 5:
            v = 0
            carry = 1
        else:
            carry = 0
        p.append(v)

        value //= 5
    if carry != 0:
        p.append(carry)

    print(p)
    s = "".join(RDIGITS[v] for v in p)

    return s[::-1]

total = 0
for line in lines:
    n = from_snafu(line)
    print(line, n)
    total += n

print(to_snafu(total), total)

