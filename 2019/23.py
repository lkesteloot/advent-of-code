
import time
from intcode import Intcode, parse_mem

COMPUTER_COUNT = 50

class IntcodeNetwork(Intcode):
    def __init__(self, mem):
        super().__init__(mem)
        self.inputs = []
        self.outputs = []
        self.empty_input_count = 0

    def input(self):
        if self.inputs:
            self.empty_input_count = 0
            return self.inputs.pop(0)
        else:
            self.empty_input_count += 1
            return -1

    def output(self, v):
        self.empty_input_count = 0
        self.outputs.append(v)

    def is_idle(self):
        return not self.inputs and self.empty_input_count > 1

data = open("input-23.txt").read()
MEM = parse_mem(data)

def do_part(part):
    computers = []
    nat = [None, None]
    last_nat = [None, None]

    for i in range(COMPUTER_COUNT):
        computer = IntcodeNetwork(MEM)
        computer.inputs.append(i)
        computers.append(computer)

    any_running = True
    while any_running:
        any_running = False
        all_idle = True
        for computer in computers:
            if not computer.halted:
                any_running = True
                computer.step()

                if len(computer.outputs) == 3:
                    destination, x, y = computer.outputs
                    computer.outputs = []

                    if destination == 255:
                        if part == 1:
                            return y
                        nat = [x, y]
                    else:
                        computers[destination].inputs.extend([x, y])

                if not computer.is_idle():
                    all_idle = False

        if part == 2 and all_idle:
            if nat[1] == last_nat[1]:
                return nat[1]
            computers[0].inputs.extend(nat)
            last_nat = nat

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
