
def parse_mem(data):
    return list(map(int, data.split(",")))

def run(mem, input_fn=None, output_fn=None):
    pc = 0
    modes = 0

    def fetch():
        nonlocal pc, mem
        value = mem[pc]
        pc += 1
        return value

    def get_parameter():
        nonlocal modes, mem
        v = fetch()
        mode = modes % 10
        modes //= 10
        if mode == 0:
            return mem[v]
        elif mode == 1:
            return v
        else:
            raise Exception()

    while True:
        opcode_slot = fetch()
        opcode = opcode_slot % 100
        modes = opcode_slot // 100

        if opcode == 1:
            # Add.
            op1 = get_parameter()
            op2 = get_parameter()
            mem[fetch()] = op1 + op2
        elif opcode == 2:
            # Multiply.
            op1 = get_parameter()
            op2 = get_parameter()
            mem[fetch()] = op1 * op2
        elif opcode == 3:
            # Input.
            mem[fetch()] = input_fn()
        elif opcode == 4:
            # Output.
            output_fn(get_parameter())
        elif opcode == 99:
            # Halt.
            break
        else:
            raise Exception(f"Unknown opcode {opcode}")

if __name__ == "__main__":
    data = "1002,4,3,4,33"
    mem = parse_mem(data)
    run(mem)
    print(mem)

