
import time
from itertools import *
from intcode import IntcodeLists, parse_mem

data = open("input-7.txt").read()
MEM = parse_mem(data)

def do_part(part):
    max_thruster = -1

    if part == 1:
        for phases in permutations(range(5)):
            previous_input = 0
            for machine in range(len(phases)):
                inputs = [phases[machine], previous_input]
                machine = IntcodeLists(MEM, inputs)
                outputs = machine.run()
                previous_input = outputs[0]
            max_thruster = max(max_thruster, previous_input)
    else:
        for phases in permutations(range(5, 10)):
            MACHINE_COUNT = len(phases)

            machines = [IntcodeLists(MEM, [phases[machine_number]])
                        for machine_number in range(MACHINE_COUNT)]
            machines[0].inputs.append(0)

            while True:
                any_stepped = False
                for i in range(MACHINE_COUNT):
                    if machines[i].can_step():
                        machines[i].step()
                        any_stepped = True
                for i in range(MACHINE_COUNT):
                    prev_machine = machines[(i - 1) % MACHINE_COUNT]
                    machines[i].inputs.extend(prev_machine.outputs)
                    prev_machine.outputs = []
                if not any_stepped:
                    break

            thruster = machines[0].inputs[0]
            max_thruster = max(max_thruster, thruster)

    return max_thruster

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
