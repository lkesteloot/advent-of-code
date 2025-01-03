
import time

data = open("input-2-test.txt").read()
data = open("input-2.txt").read()

MEM = list(map(int, data.split(",")))

def run(mem):
    pc = 0

    def fetch():
        nonlocal pc
        value = mem[pc]
        pc += 1
        return value

    while (opcode := fetch()) != 99:
        if opcode == 1:
            op1 = mem[fetch()]
            op2 = mem[fetch()]
            mem[fetch()] = op1 + op2
        elif opcode == 2:
            op1 = mem[fetch()]
            op2 = mem[fetch()]
            mem[fetch()] = op1 * op2
        else:
            raise Exception()

def do_part(part):
    global MEM

    if part == 1:
        mem = MEM[:]
        mem[1] = 12
        mem[2] = 2
        run(mem)
        return mem[0]
    else:
        for noun in range(100):
            for verb in range(100):
                mem = MEM[:]
                mem[1] = noun
                mem[2] = verb
                run(mem)
                if mem[0] == 19690720:
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
