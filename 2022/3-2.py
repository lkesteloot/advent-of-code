
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

line_number = 0
total = 0

badge = None
for line in lines:
    s = set(line)
    if badge is None:
        badge = s
    else:
        badge = s.intersection(badge)

    if line_number == 2:
        print(badge)
        if len(badge) != 1:
            print("error", badge)
        else:
            ch = list(badge)[0]
            if ch >= "a" and ch <= "z":
                score = ord(ch) - ord("a") + 1
            elif ch >= "A" and ch <= "Z":
                score = ord(ch) - ord("A") + 27
            else:
                print("error")
            total += score
        badge = None
        line_number = 0
    else:
        line_number += 1

print(total)


