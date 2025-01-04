
import time
from intcode import Intcode, IntcodeLists, parse_mem

data = open("input-9-test.txt").read()
data = open("input-9.txt").read()

MEM = parse_mem(data)

def do_part(part):
    mode = part
    machine = IntcodeLists(MEM, [mode])
    output = machine.run()
    if len(output) > 1:
        print(output)
    return output[0]

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
