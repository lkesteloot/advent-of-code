
# mv ~/Downloads/input.txt input-20.txt

import sys
from collections import defaultdict
from itertools import *
from functools import *
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-20.txt")]

iea = lines[0]
lines = lines[2:]

def pad(lines, padchar):
    out = []
    out.append(padchar*(len(lines[0]) + 2))
    out.extend(padchar + line + padchar for line in lines)
    out.append(padchar*(len(lines[0]) + 2))
    return out

def clip(lines):
    lines = [line[1:-1] for line in lines[1:-1]]
    return lines

def process(lines, padchar):
    lines = pad(lines, padchar)
    lines = pad(lines, padchar)
    lines = pad(lines, padchar)
    lines = pad(lines, padchar)
    print("Padded:")
    print("\n".join(lines))
    print()
    width = len(lines[0])
    height = len(lines)

    out = [["." for x in range(width)] for y in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            v = ""
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    v += "1" if lines[y + dy][x + dx] == "#" else "0"
            v = int(v, 2)
            out[y][x] = iea[v]

    out = ["".join(line) for line in out]
    out = clip(out)
    print("Output:")
    print("\n".join(out))
    print()
    return out

print("\n".join(lines))
print()
for i in range(25):
    lines = process(lines, ".")
    lines = process(lines, iea[0])
count = "".join(lines).count("#")
print(count)

