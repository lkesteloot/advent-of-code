
import time
from intcode import Intcode, parse_mem

data = open("input-2-test.txt").read()
data = open("input-2.txt").read()

MEM = parse_mem(data)

def do_part(part):
    global MEM

    if part == 1:
        mem = MEM[:]
        mem[1] = 12
        mem[2] = 2
        machine = Intcode(mem)
        machine.run()
        return machine.mem[0]
    else:
        for noun in range(100):
            for verb in range(100):
                mem = MEM[:]
                mem[1] = noun
                mem[2] = verb
                machine = Intcode(mem)
                machine.run()
                if machine.mem[0] == 19690720:
                    return 100*noun + verb

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
