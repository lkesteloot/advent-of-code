
import re
from collections import defaultdict

lines = [line.strip() for line in open("input-3.txt")]

gear_at = defaultdict(lambda: [])

for line_number, line in enumerate(lines):
    for m in re.finditer(r"[0-9]+", line):
        begin, end = m.span()
        value = int(m.group(0))

        for x in range(max(begin - 1, 0), min(end + 1, len(line))):
            for y in range(max(line_number - 1, 0), min(line_number + 2, len(lines))):
                if lines[y][x] == "*":
                    gear_at["%d,%d" % (x, y)].append(value)

print(sum(v[0]*v[1] for v in gear_at.values() if len(v) == 2))
