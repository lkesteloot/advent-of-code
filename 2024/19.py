
import time
from functools import *

data = open("input-19-test.txt").read()
data = open("input-19.txt").read()

available, wanted = data.split("\n\n")
available = available.split(", ")
wanted = wanted.splitlines()

@cache
def how_many_ways_possible(w):
    if w == "":
        return 1

    return sum(how_many_ways_possible(w[len(a):])
               for a in available
               if w.startswith(a))

def do_part(part):
    return sum(1 if part == 1 else count
               for w in wanted
               if (count := how_many_ways_possible(w)) > 0)

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
