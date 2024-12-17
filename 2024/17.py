
import time

data = open("input-17-test.txt").read()
data = open("input-17-test-2.txt").read()
data = open("input-17.txt").read()

numbers = list(map(int, data.split(",")))
a, b, c, *opcodes = numbers

def do_part_1(a, b, c, opcodes):
    pc = 0
    output = []

    def combo(operand):
        return [0, 1, 2, 3, a, b, c][operand]

    while True:
        if pc >= len(opcodes):
            break

        opcode = opcodes[pc]
        pc += 1
        operand = opcodes[pc]
        pc += 1
        if opcode == 0:
            a = a // (2 ** combo(operand))
        elif opcode == 1:
            b = b ^ operand
        elif opcode == 2:
            b = combo(operand) & 0x07
        elif opcode == 3:
            if a != 0:
                pc = operand
        elif opcode == 4:
            b = b ^ c
        elif opcode == 5:
            output.append(combo(operand) & 0x07)
        elif opcode == 6:
            b = a // (2 ** combo(operand))
        elif opcode == 7:
            c = a // (2 ** combo(operand))
        else:
            raise Exception()

    return ",".join(map(str, output))

def do_part_2(opcodes):
    candidates = []

    def add_3_bits(a, i):
        if i < 0:
            candidates.append(a)
            return
        for bits in range(8):
            new_a = (a << 3) | bits
            output = (new_a ^ (new_a >> (7 - (new_a & 7)))) & 7
            if output == opcodes[i]:
                add_3_bits(new_a, i - 1)

    add_3_bits(0, len(opcodes) - 1)
    return min(candidates)

def do_part(part):
    if part == 1:
        return do_part_1(a, b, c, opcodes)
    else:
        return do_part_2(opcodes)

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
