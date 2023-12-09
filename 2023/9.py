
from more_itertools import pairwise

lines = open("input-9.txt").read().splitlines()

def find_next(s):
    s = list(s)
    if all(i == 0 for i in s):
        return 0
    return s[0] - find_next(b - a for a, b in pairwise(s))

print(sum(find_next(int(i) for i in line.split()) for line in lines))
