
# mv ~/Downloads/input.txt input-24.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-24.txt")]

def get_last(s):
    return s.split(" ")[-1]

if False:
    steps = []
    for i in range(14):
        steps.append(lines[i*18:(i + 1)*18])

    for step in range(18):
        for digit in range(14):
            if steps[0][step] != steps[digit][step]:
                print(", ".join([get_last(s[step]) for s in steps]))
                break
        else:
            # All same
            pass

Z = [1, 1, 1, 1, 26, 26, 1, 26, 1, 26, 1, 26, 26, 26]
A = [13, 11, 11, 10, -14, -4, 11, -3, 12, -12, 13, -12, -15, -12]
B = [10, 16, 0, 13, 7, 11, 11, 10, 16, 8, 15, 2, 5, 10]

def go(INPUT):
    z = 0
    for i in range(14):
        w = int(INPUT[i])
        x = z%26 + A[i]
        z //= Z[i]
        happens = x != w
        print(i, w, z, z%26, x, w, happens)
        if happens:
            z = z*26 + w + B[i]
    return z


# w3 = w4 + 1
# w2 = w5 + 4
# w6 + 8 = w7
# w8 + 4 = w9
# w10 + 3 = w11
# w1 + 1 = w12
# w0 = w13 + 2

#INPUT = "98998519596997" # largest

#        01234567890123
INPUT = "31521119151421" # smallest
print(INPUT, go(INPUT))

if False:
    for i in range(14):
        print("x = z%%26 + %d;" % A[i])
        print("z /= %d;" % Z[i])
        print("if (x != w%d) {" % i)
        print("    z = z*26 + w%d + %d;" % (i, B[i]))
        print("}")
