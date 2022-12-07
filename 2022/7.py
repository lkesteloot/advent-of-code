
# mv ~/Downloads/input.txt input-xx.txt

import sys
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-7-test.txt")]
lines = [line.strip() for line in open("input-7.txt")]
disk_size = 70000000
needed = 30000000

sizes = defaultdict(lambda: 0)

def parent(d):
    i = d.rindex("/")
    if i == 0:
        d = "/"
    else:
        d = d[:i]
    return d

d = "/"
for line in lines:
    print(line, d)
    if line.startswith("$ cd "):
        subdir = line[5:]
        if subdir == "..":
            print(d)
            d = parent(d)
        elif subdir == "/":
            d = "/"
        else:
            if d != "/":
                d += "/"
            d += subdir
    elif line.startswith("$ ls"):
        pass
    else:
        size, filename = line.split(" ")
        if size == "dir":
            pass
        else:
            sizes[d] += int(size)
print(sizes)
total_sizes = defaultdict(lambda: 0)
for d, size in sizes.items():
    total_sizes[d] += size
    while d != "/":
        d = parent(d)
        total_sizes[d] += size
print(total_sizes)

t = 0
for d, size in total_sizes.items():
    if size <= 100000:
        t += size
print(t)

total_used = total_sizes["/"]
free = disk_size - total_used

min_dir = None
min_size = disk_size
for d, size in total_sizes.items():
    if free + size >= needed and size < min_size:
        min_size = size
        min_dir = d
print(min_dir, min_size)

