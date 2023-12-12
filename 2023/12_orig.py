
# mv ~/Downloads/input.txt input-12.txt

import sys, re
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
# import numpy as np
# import scipy.signal

lines = open("input-12-test.txt").read().splitlines()
lines = open("input-12.txt").read().splitlines()
# matrix = [list(map(int, list(line))) for line in lines]
# name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
# grid = np.array([list(line) for line in lines])
# yxs = (yx for yx, ch in np.ndenumerate(grid) if is_symbol(ch))

part2 = True

@cache
def go(pattern, counts, expect):
    #print(indent, "go", pattern, counts, expect)
    if pattern.find("#") == -1 and len(counts) == 0:
        return 1
    if pattern.find("#") >= 0 and len(counts) == 0:
        #print(indent, "go", pattern, counts, expect)
        return 0
    if pattern.strip(".") == "" and len(counts) > 0:
        #print(indent, "go", pattern, counts, expect)
        return 0

    if pattern[0] == ".":
        if expect == "#":
            return 0
        return go(pattern.lstrip("."), counts, "any")
    elif pattern[0] == "#":
        if expect == ".":
            return 0
        new_count = counts[0] - 1
        if new_count == 0:
            return go(pattern[1:], counts[1:], ".")
        else:
            return go(pattern[1:], (new_count,) + counts[1:], "#")
    else:
        if expect != "#":
            as_dot = go("." + pattern[1:], counts, "any")
        else:
            as_dot = 0
        if expect != ".":
            as_hash = go("#" + pattern[1:], counts, "any")
        else:
            as_hash = 0
        return as_hash + as_dot

def go2(pattern, counts):
    counts = tuple(counts)

    # key is: ((counts),expect), value is total
    states = {
        (counts, "any"): 1,
    }

    for ch in pattern:
        new_states = defaultdict(int)

        for (counts, expect), total in states.items():
            if ch == "#" or ch == "?":
                if (expect == "any" or expect == "#") and len(counts) > 0:
                    new_count = counts[0] - 1
                    if new_count == 0:
                        key = counts[1:], "."
                    else:
                        key = (new_count,) + counts[1:], "#"
                    new_states[key] += total
            if ch == "." or ch == "?":
                if expect == "any" or expect == ".":
                    key = counts, "any"
                    new_states[key] += total

        states = new_states

    return sum(total for (counts, expect), total in states.items() if len(counts) == 0)

total_go = 0
total_go2 = 0
for num, line in enumerate(lines):
    pattern, counts = line.split()
    if part2:
        pattern = "?".join(p for p in [pattern]*5)
        counts = ",".join([counts]*5)
    pattern = pattern.strip(".")
    counts = list(map(int, counts.split(",")))
    if True:
        qq = go(pattern, tuple(counts), "any")
        print("go", pattern, counts, qq)
        total_go += qq
    if True:
        qq = go2(pattern, counts)
        print("go2", pattern, counts, qq)
        total_go2 += qq
    if False:
        #print(pattern, counts)
        regex = "^\.*" + r"\.+".join("#"*count for count in counts) + "\.*$"
        r = re.compile(regex)
        chs = list(pattern)
        qs = [i for i, ch in enumerate(chs) if ch == "?"]
        opts = [(0, 1) for i in range(len(qs))]
        #print(pattern, counts, regex, qs, opts)
        qqq = 0
        for opt in product(*opts):
            #print(opt)
            for i in range(len(qs)):
                chs[qs[i]] = "#" if opt[i] else "."
            s = "".join(chs)
            if r.fullmatch(s):
                #print(opt, s)
                qqq += 1
        if qq != qqq:
            print("--------------------", pattern, counts, qq, qqq)
    print(num, total_go, total_go2)
    #break
print(total_go, total_go2)
