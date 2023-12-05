
# mv ~/Downloads/input.txt input-xx.txt

import sys, re
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-xx-test.txt")]
#lines = [line.strip() for line in open("input-xx.txt")]
# matrix = [list(map(int, list(line))) for line in lines]
# name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
# grid = np.array([list(line) for line in lines])
# yxs = (yx for yx, ch in np.ndenumerate(grid) if is_symbol(ch))

for line_number, line in enumerate(lines):
#    for m in re.finditer(r"[0-9]+", line):
#        begin, end = m.span()
#        value = int(m.group(0))

