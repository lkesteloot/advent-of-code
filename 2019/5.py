
import time
from intcode import IntcodeLists, parse_mem

data = open("input-5.txt").read()

MEM = parse_mem(data)

def do_part(part):
    system_id = 1 if part == 1 else 5

    machine = IntcodeLists(MEM, [system_id])
    outputs = machine.run()

    if any(outputs[:-1]):
        print("Diagnostics failed", outputs)

    return outputs[-1]

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
