
# mv ~/Downloads/input.txt input-8.txt

import math

lines = open("input-8.txt").read().splitlines()

steps = lines[0]
lines = lines[2:]

mapping = {}
for line in lines:
    node = line[:3]
    left = line[7:10]
    right = line[12:15]
    mapping[node] = (left, right)

nodes = [node for node in mapping.keys() if node.endswith("A")]
step_counts = []
for node in nodes:
    step_count = 0
    while not node.endswith("Z"):
        node = mapping[node][0 if steps[step_count % len(steps)] == "L" else 1]
        step_count += 1
    step_counts.append(step_count)
print(math.lcm(*step_counts))


