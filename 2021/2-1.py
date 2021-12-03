
from functools import reduce
from math import prod

print(prod(reduce(lambda acc, x:
        (acc[0] + x[1], acc[1]) if x[0] == "forward"
        else (acc[0], acc[1] + x[1]) if x[0] == "down"
        else (acc[0], acc[1] - x[1]),
            map(lambda parts: (parts[0], int(parts[1])),
                [line.strip().split() for line in open("input-2.txt")]),
        (0, 0))))

