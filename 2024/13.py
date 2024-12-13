
import time, re
import numpy as np

data = open("input-13-test.txt").read()
data = open("input-13.txt").read()

PART_2_OFFSET = np.array([10000000000000, 10000000000000])

def is_int(x):
    return abs(x - round(x)) < 0.001

def do_part(part):
    total = 0

    blocks = data.split("\n\n")
    for block in blocks:
        lines = block.splitlines()
        ax, ay = re.findall(r"([0-9]+)", lines[0])
        bx, by = re.findall(r"([0-9]+)", lines[1])
        cx, cy = re.findall(r"([0-9]+)", lines[2])

        m = np.array([[ax, bx], [ay, by]], dtype=float)
        p = np.array([cx, cy], dtype=float)
        if part == 2:
            p += PART_2_OFFSET

        q = np.linalg.solve(m, p)
        if is_int(q[0]) and is_int(q[1]):
            total += q[0]*3 + q[1]*1

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
