
from itertools import *
from more_itertools import *

size = 10

lines = [line.strip() for line in open("input-11.txt")]
o = list(list(map(int, list(line))) for line in lines)
print(o)

flash_count = 0
step = 0
while True:
    step += 1
    flashed = []
    for i in range(size):
        flashed.append([False]*size)

    for y in range(size):
        for x in range(size):
            o[y][x] += 1

    something_flashed = True
    ff = 0
    while something_flashed:
        something_flashed = False

        for y in range(size):
            for x in range(size):
                if o[y][x] > 9 and not flashed[y][x]:
                    flashed[y][x] = True
                    something_flashed = True
                    flash_count += 1
                    ff += 1

                    if x > 0: o[y][x - 1] += 1
                    if x > 0 and y > 0: o[y - 1][x - 1] += 1
                    if x > 0 and y < size - 1: o[y + 1][x - 1] += 1
                    if x < size - 1: o[y][x + 1] += 1
                    if x < size - 1 and y > 0: o[y - 1][x + 1] += 1
                    if x < size - 1 and y < size - 1: o[y + 1][x + 1] += 1
                    if y > 0: o[y - 1][x] += 1
                    if y < size - 1: o[y + 1][x] += 1

    for y in range(size):
        for x in range(size):
            if flashed[y][x]:
                o[y][x] = 0

    if ff == 100:
        print("all flashed", step)
        break

print(flash_count)
