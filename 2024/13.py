
import time, re
import numpy as np

data = open("input-13-test.txt").read()
data = open("input-13.txt").read()

PART_2_OFFSET = 10000000000000

def is_int(x):
    return abs(x - round(x)) < 0.001

def do_part(part):
    total = 0

    blocks = data.split("\n\n")
    for block in blocks:
        a, b, p = (re.findall(r"\d+", line) for line in block.strip().splitlines())

        m = np.array([a, b], dtype=int).T
        p = np.array(p, dtype=int)
        if part == 2:
            p += PART_2_OFFSET

        a, b = np.linalg.solve(m, p)
        if is_int(a) and is_int(b):
            total += a*3 + b*1

    return int(total)

def main():
    for part in [1, 2]:
        before = time.perf_counter()
        answer = do_part(part)
        after = time.perf_counter()
        elapsed = round((after - before)*1_000_000)
        unit = "µs"
        if elapsed >= 1000:
            elapsed //= 1000
            unit = "ms"
        print(f"Part {part}: {answer} ({elapsed:,} {unit})")

main()
