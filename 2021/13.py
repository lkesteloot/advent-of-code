
# from itertools import *
# from more_itertools import *
# import numpy as np
# import scipy.signal

lines = [line.strip() for line in open("input-13.txt")]

dots = set()
insts = []

for line in lines:
    if "," in line:
        x, y = line.split(",")
        x = int(x)
        y = int(y)
        dots.add( (x, y) )
    elif line.startswith("fold along"):
        line = line[11:]
        axis, value = line.split("=")
        value = int(value)
        insts.append( (axis, value) )

print(dots)
print(insts)

for axis, value in insts:
    new_dots = set()

    if axis == "y":
        for x, y in dots:
            if y > value:
                y = 2*value - y
            new_dots.add( (x, y) )
    elif axis == "x":
        for x, y in dots:
            if x > value:
                x = 2*value - x
            new_dots.add( (x, y) )

    dots = new_dots
    print(len(dots))

width = max(x for (x, y) in dots) + 1
height = max(y for (x, y) in dots) + 1


print(width, height)

for y in range(height):
    line = []
    for x in range(width):
        line.append("#" if (x, y) in dots else " ")
    print("".join(line))
