

# mv ~/Downloads/input.txt input-22.txt

import sys, re, time
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
import numpy as np
# import scipy.signal

lines = open("input-22-test.txt").read().splitlines()
lines = open("input-22-test-2.txt").read().splitlines()
#lines = open("input-22.txt").read().splitlines()
# width = len(lines[0])
# height = len(lines)
# matrix = [list(map(int, list(line))) for line in lines]
# name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
# grid = np.array([list(line) for line in lines])
# grid = np.pad(grid, 1, constant_values=-1)
# yxs = (yx for yx, ch in np.ndenumerate(grid) if is_symbol(ch))
# tiles = {(x, y): lines[y][x] for y in range(height) for x in range(width)}
# rolls = {(x, y) for y in range(height) for x in range(width) if lines[y][x] == "O"}
#    for m in re.finditer(r"[0-9]+", line):
#        begin, end = m.span()
#        value = int(m.group(0))

INITIAL = np.array(lines, int)

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def get_next_secret(secret):
    secret = prune(mix(secret*64, secret))
    secret = prune(mix(secret//32, secret))
    secret = prune(mix(secret*2048, secret))
    return secret

def do_part(part):
    count = len(lines)
    secret = np.empty( (count, 2001), dtype=int)
    secret[:,0] = INITIAL
    for i in range(2000):
        secret[:,i+1] = get_next_secret(secret[:,i])

    if part == 1:
        return secret[:,-1].sum()
    else:
        ones_digit = secret % 10
        diff = ones_digit[:,1:] - ones_digit[:,:-1]
        width = diff.shape[1]

        # key is (row,a,b), value is list of indices of diff.
        prefix = defaultdict(list)
        for row in range(count):
            for i in range(width - 3):
                a = diff[row,i]
                b = diff[row,i+1]
                c = diff[row,i+2]
                d = diff[row,i+3]
                prefix[(row,a,b,c,d)].append(i)
        print(len(prefix))

        best_tuple = None
        best_total = 0
        for a in range(-9, 10):
            print(a)
            for b in range(-9, 10):
                for c in range(-9, 10):
                    for d in range(-9, 10):
                        total = 0
                        for row in range(count):
                            for i in prefix[(row, a, b, c, d)]:
                                total += ones_digit[row,i+3+1]
                                break
                        if total > best_total:
                            best_total = total
                            best_tuple = a, b, c, d
                            print(best_total, best_tuple)

        # not 2261
        return best_total

def main():
    for part in [1, 2]:
        before = time.perf_counter()
        answer = do_part(part)
        after = time.perf_counter()
        elapsed = round((after - before)*1_000_000)
        unit = "µs"
        if elapsed >= 1000:
            elapsed //= 1000
            unit = "ms"
        print(f"Part {part}: {answer} ({elapsed:,} {unit})")

main()
