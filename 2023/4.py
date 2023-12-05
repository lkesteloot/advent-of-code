
import re

lines = [line.strip() for line in open("input-4-test.txt")]
lines = [line.strip() for line in open("input-4.txt")]
print(len(lines))

# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53

copies = [1]*len(lines)

for num, line in enumerate(lines):
	line = line.split(": ")[1]
	left, right = line.split(" | ")
	left = [int(n) for n in left.split()]
	right = set(int(n) for n in right.split())
	s = sum(1 for n in left if n in right)
	for i in range(num + 1, num + 1 + s):
		copies[i] += copies[num]

print(sum(copies))
