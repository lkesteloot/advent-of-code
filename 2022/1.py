
# mv ~/Downloads/input.txt input-xx.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-1.txt")]
# matrix = [list(map(int, list(line))) for line in lines]

cals = []
total = 0
for line in lines:
    if line == "":
        cals.append(total)
        total = 0
    else:
        total += int(line)

cals.sort()
print(sum(cals[-3:]))

