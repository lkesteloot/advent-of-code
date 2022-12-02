
# mv ~/Downloads/input.txt input-xx.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-xx-test.txt")]
matrix = [list(map(int, list(line))) for line in lines]

