
TRON = False

def parse_mem(data):
    return list(map(int, data.split(",")))

def run(mem, input_fn=None, output_fn=None):
    pc = 0
    modes = 0

    def fetch():
        nonlocal pc, mem
        value = mem[pc]
        if TRON:
            print(f"TRON: fetch({pc}) -> {value}")
        pc += 1
        return value

    def get_parameter():
        nonlocal modes, mem
        imm = fetch()
        mode = modes % 10
        modes //= 10
        if mode == 0:
            value = mem[imm]
        elif mode == 1:
            value = imm
        else:
            raise Exception()

        if TRON:
            print(f"TRON: get_parameter({pc}, {mode}) -> {imm} -> {value}")

        return value

    while True:
        if TRON:
            print("---", pc, mem)

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
        elif opcode == 5:
            # Jump if true.
            value = get_parameter()
            location = get_parameter()
            if value:
                pc = location
        elif opcode == 6:
            # Jump if false.
            value = get_parameter()
            location = get_parameter()
            if not value:
                pc = location
        elif opcode == 7:
            # Less than.
            op1 = get_parameter()
            op2 = get_parameter()
            mem[fetch()] = int(op1 < op2)
        elif opcode == 8:
            # Equals.
            op1 = get_parameter()
            op2 = get_parameter()
            mem[fetch()] = int(op1 == op2)
        elif opcode == 99:
            # Halt.
            break
        else:
            raise Exception(f"Unknown opcode {opcode}")

def run_with_io(mem, inputs):
    inputs = inputs[:]
    outputs = []

    run(mem, input_fn=lambda: inputs.pop(0), output_fn=outputs.append)

    return outputs

if __name__ == "__main__":
    data = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
    mem = parse_mem(data)
    run(mem, input_fn=lambda: 0, output_fn=print)
    print(mem)

