
from functools import cache

lines = open("input-12.txt").read().splitlines()

part2 = True

@cache
def go(pattern, counts, expect):
    if pattern == "":
        return 1 if len(counts) == 0 else 0

    total = 0
    if pattern[0] == "." or pattern[0] == "?":
        if expect != "#":
            total += go(pattern[1:], counts, "any")
    if pattern[0] == "#" or pattern[0] == "?":
        if expect != "." and len(counts) > 0:
            new_count = counts[0] - 1
            if new_count == 0:
                total += go(pattern[1:], counts[1:], ".")
            else:
                total += go(pattern[1:], (new_count,) + counts[1:], "#")

    return total

grand_total = 0
for num, line in enumerate(lines):
    pattern, counts = line.split()
    if part2:
        pattern = "?".join(p for p in [pattern]*5)
        counts = ",".join([counts]*5)
    pattern = pattern.strip(".")
    counts = list(map(int, counts.split(",")))
    grand_total += go(pattern, tuple(counts), "any")
print(grand_total)
