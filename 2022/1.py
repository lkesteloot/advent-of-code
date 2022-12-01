
from more_itertools import *

lines = [line.strip() for line in open("input-1.txt")]

cals = split_at(lines, lambda line: line == "")
cals = sorted(sum(int(cal) for cal in elf) for elf in cals)
print(cals[-1])
print(sum(cals[-3:]))

