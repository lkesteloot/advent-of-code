
import numpy as np

lines = open("input-1-test.txt").read().splitlines()
lines = open("input-1.txt").read().splitlines()

v = np.array([[int(f) for f in line.split()] for line in lines]).T

# Part 1.
sv = np.sort(v)
print("Part 1:", np.sum(np.absolute(sv[0] - sv[1])))

# Part 2.
v1, v2 = np.meshgrid(v[0], v[1])
print("Part 2:", np.sum(np.count_nonzero(v1 == v2, axis=0) * v[0]))
