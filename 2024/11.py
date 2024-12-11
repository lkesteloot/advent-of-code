
import time
from functools import *

line = open("input-11-test.txt").read()
line = open("input-11.txt").read()

INITIAL_VALUES = list(map(int, line.split()))

@cache
def go(value, steps):
    if steps == 0:
        return 1

    if value == 0:
        return go(1, steps - 1)

    s = str(value)
    if len(s) % 2 == 0:
        half = len(s) // 2
        return go(int(s[:half]), steps - 1) + go(int(s[half:]), steps - 1)

    return go(value*2024, steps - 1)

def do_part(part):
    steps = [25, 75][part - 1]
    return sum(go(value, steps) for value in INITIAL_VALUES)

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
