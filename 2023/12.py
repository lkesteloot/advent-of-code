
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

    if True:
        # (pattern_index, count_index) => total
        states = {
            (0, 0): 1,
        }

        sub_total = 0
        pattern += "."
        while states:
            new_states = defaultdict(int)

            for (pattern_index, count_index), total in states.items():
                if count_index == len(counts):
                    if pattern_index == len(pattern):
                        sub_total += total
                else:
                    count = counts[count_index]
                    if pattern[pattern_index:pattern_index + count].replace("?", "#") == "#"*count and \
                            pattern[pattern_index + count] != "#":

                        new_states[pattern_index + count + 1, count_index + 1] += total
                if pattern_index < len(pattern) and (pattern[pattern_index] == "." or pattern[pattern_index] == "?"):
                    new_states[pattern_index + 1, count_index] += total

            states = new_states

        grand_total += sub_total
    else:
        # Dynamic programming solution.
        pattern += "."
        grid = [[0]*(len(pattern) + 1) for i in range(len(counts) + 1)]
        grid[0][0] = 1

        for pattern_index in range(len(pattern)):
            for count_index in range(len(counts) + 1):
                total = grid[count_index][pattern_index]
                if total > 0:
                    if count_index < len(counts):
                        count = counts[count_index]
                        if pattern[pattern_index:pattern_index + count].replace("?", "#") == "#"*count and \
                                pattern[pattern_index + count] != "#":

                            grid[count_index + 1][pattern_index + count + 1] += total
                    if pattern[pattern_index] != "#":
                        grid[count_index][pattern_index + 1] += total

        grand_total += grid[-1][-1]

print(grand_total)
