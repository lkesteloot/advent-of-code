

# mv ~/Downloads/input.txt input-5.txt

import sys, re, time
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
import numpy as np
# import scipy.signal
from intcode import run, parse_mem

data = open("input-5.txt").read()

MEM = parse_mem(data)

def do_part(part):
    if part == 1:
        mem = MEM[:]

        outputs = []
        run(mem, input_fn=lambda: 1, output_fn=outputs.append)

        if any(outputs[:-1]):
            print("Diagnostics failed", outputs)

        return outputs[-1]

def main():
    for part in [1]:
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
