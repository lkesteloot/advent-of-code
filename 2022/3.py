
# mv ~/Downloads/input.txt input-xx.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-3.txt")]
# matrix = [list(map(int, list(line))) for line in lines]

total = 0

for line in lines:
    first = line[:len(line)//2]
    second = line[len(line)//2:]

    first = set(first)
    print(first)
    found = set()
    for ch in second:
        if ch in first:
            found.add(ch)

    if len(found) != 1:
        print("error", found)
    else:
        ch = list(found)[0]
        if ch >= "a" and ch <= "z":
            score = ord(ch) - ord("a") + 1
        elif ch >= "A" and ch <= "Z":
            score = ord(ch) - ord("A") + 27
        else:
            print("error")
        total += score

print(total)


