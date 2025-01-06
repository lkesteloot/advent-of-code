
TRON = False

def parse_mem(data):
    return list(map(int, data.split(",")))

class Intcode:
    def __init__(self, mem):
        self.mem = dict(enumerate(mem))
        self.pc = 0
        self.halted = False
        self.relative_base = 0

    def step(self):
        if TRON:
            print("---", self.pc, self.mem)

        opcode_slot = self.fetch()
        modes, opcode = divmod(opcode_slot, 100)

        def get_parameter_address():
            nonlocal modes
            pc = self.pc
            imm = self.fetch()
            mode = modes % 10
            modes //= 10
            if mode == 0:
                address = imm
            elif mode == 1:
                raise Exception()
            elif mode == 2:
                address = self.relative_base + imm
            else:
                raise Exception()

            if TRON:
                print(f"TRON: get_parameter_address({pc}, {mode}) -> {imm} -> {address}")

            return address

        def get_parameter():
            nonlocal modes
            pc = self.pc
            imm = self.fetch()
            mode = modes % 10
            modes //= 10
            if mode == 0:
                value = self.read_memory(imm)
            elif mode == 1:
                value = imm
            elif mode == 2:
                value = self.read_memory(self.relative_base + imm)
            else:
                raise Exception()

            if TRON:
                print(f"TRON: get_parameter({pc}, {mode}) -> {imm} -> {value}")

            return value

        if opcode == 1:
            # Add.
            op1 = get_parameter()
            op2 = get_parameter()
            self.write_memory(get_parameter_address(), op1 + op2)
        elif opcode == 2:
            # Multiply.
            op1 = get_parameter()
            op2 = get_parameter()
            self.write_memory(get_parameter_address(), op1 * op2)
        elif opcode == 3:
            # Input.
            self.write_memory(get_parameter_address(), self.input())
        elif opcode == 4:
            # Output.
            self.output(get_parameter())
        elif opcode == 5:
            # Jump if true.
            value = get_parameter()
            location = get_parameter()
            if value:
                self.pc = location
        elif opcode == 6:
            # Jump if false.
            value = get_parameter()
            location = get_parameter()
            if not value:
                self.pc = location
        elif opcode == 7:
            # Less than.
            op1 = get_parameter()
            op2 = get_parameter()
            self.write_memory(get_parameter_address(), int(op1 < op2))
        elif opcode == 8:
            # Equals.
            op1 = get_parameter()
            op2 = get_parameter()
            self.write_memory(get_parameter_address(), int(op1 == op2))
        elif opcode == 9:
            # Adjust relative base.
            self.relative_base += get_parameter()
        elif opcode == 99:
            # Halt.
            self.halted = True
        else:
            raise Exception(f"Unknown opcode {opcode}")

    def run(self):
        while not self.halted:
            self.step()

    def at_input_opcode(self):
        return self.read_memory(self.pc) % 100 == 3

    def fetch(self):
        value = self.read_memory(self.pc)
        if TRON:
            print(f"TRON: fetch({self.pc}) -> {value}")
        self.pc += 1
        return value

    def read_memory(self, address):
        return self.mem.get(address, 0)

    def write_memory(self, address, value):
        self.mem[address] = value

class IntcodeLists(Intcode):
    def __init__(self, mem, inputs):
        super().__init__(mem)
        self.inputs = inputs[:]
        self.outputs = []

    def input(self):
        return self.inputs.pop(0)

    def output(self, v):
        self.outputs.append(v)

    def run(self):
        super().run()
        return self.outputs

    def can_step(self):
        return not self.halted and not (self.at_input_opcode() and not self.inputs)

if __name__ == "__main__":
    data = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
    mem = parse_mem(data)
    machine = IntcodeLists(mem, [0])
    outputs = machine.run()
    print(outputs, mem)

