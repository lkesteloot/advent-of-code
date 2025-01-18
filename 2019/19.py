
import time
from intcode import IntcodeLists, parse_mem

data = open("input-19.txt").read()
MEM = parse_mem(data)

def is_pulled(x, y):
    if x < 0 or y < 0:
        return False

    ascii = IntcodeLists(MEM, [x, y])
    outputs = ascii.run()
    return outputs[0] == 1

def do_part(part):
    if part == 1:
        return sum(is_pulled(x, y) for y in range(50) for x in range(50))
    else:
        x, y = 4, 5

        while True:
            # Guaranteed pulled here.
            if is_pulled(x + 99, y - 99):
                y -= 99
                return x*10000 + y

            y += 1
            while not is_pulled(x, y):
                x += 1

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
