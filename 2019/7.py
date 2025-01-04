
import sys, re, time
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
import numpy as np
# import scipy.signal
from intcode import run_with_io, parse_mem

data = open("input-7-test.txt").read()
data = open("input-7.txt").read()

MEM = parse_mem(data)

def do_part(part):
    max_thruster = -1

    if part == 1:
        for phases in permutations(range(5)):
            previous_input = 0
            for machine in range(len(phases)):
                mem = MEM[:]
                inputs = [phases[machine], previous_input]
                outputs = run_with_io(mem, inputs)
                previous_input = outputs[0]
            max_thruster = max(max_thruster, previous_input)
    else:
        for phases in permutations(range(5, 10)):
            machines = [MEM[:] for i in range(len(phases))]

            previous_input = 0
            for machine in range(len(phases)):
                mem = MEM[:]
                inputs = [phases[machine], previous_input]
                outputs = run_with_io(mem, inputs)
                previous_input = outputs[0]
            max_thruster = max(max_thruster, previous_input)

    return max_thruster

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
