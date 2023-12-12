
from collections import defaultdict

lines = open("input-12.txt").read().splitlines()

part2 = True

grand_total = 0
for line in lines:
    pattern, counts = line.split()

    if part2:
        pattern = "?".join([pattern]*5)
        counts = ",".join([counts]*5)

    counts = tuple(map(int, counts.split(",")))

    # key is ((counts),expect); value is total
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

    grand_total += sum(total for (counts, expect), total in states.items() if len(counts) == 0)

print(grand_total)
