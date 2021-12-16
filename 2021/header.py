
# mv ~/Downloads/input.txt input-14.txt

import sys
from collections import defaultdict
from itertools import *
from functools import *
from more_itertools import *
import numpy as np
import scipy.signal

lines = [line.strip() for line in open("input-12-test.txt")]

