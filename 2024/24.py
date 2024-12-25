
import time
from itertools import count
from functools import cache

data = open("input-24-test.txt").read()
data = open("input-24.txt").read()

def parse_initial(line):
    var, value = line.split(": ")
    return var, int(value)

def parse_gate(line):
    left, op, right, arrow, result = line.split(" ")
    return result, (left, op, right)

def sort_ops(gate):
    left, op, right = gate
    return (left, op, right) if left < right else (right, op, left)

def xor(a, b):
    return (a and not b) or (not a and b)

INITIAL, GATES = data.split("\n\n")
INITIAL = dict(map(parse_initial, INITIAL.splitlines()))
# Result to (left, op, right)
GATES = dict(map(parse_gate, GATES.splitlines()))
# (left, op, right) to gate, with left and right sorted.
GATES_REV = dict((sort_ops(gate_rule), gate) for gate, gate_rule in GATES.items())

@cache
def evaluate(var):
    value = INITIAL.get(var)
    if value is not None:
        return value

    gate = GATES.get(var)
    if gate is None:
        return None

    left, op, right = gate
    left = evaluate(left)
    right = evaluate(right)

    if op == "AND":
        value = int(left and right)
    elif op == "OR":
        value = int(left or right)
    elif op == "XOR":
        value = int(xor(left, right))
    else:
        raise Exception()

    return value

def var_of(letter, number):
    return letter + "%02d" % number

def get_gate(var1, op, var2, swaps={}):
    gate = GATES_REV.get(sort_ops( (var1, op, var2) ))
    return None if gate is None else swaps.get(gate, gate)

def with_swap(swaps, a, b):
    if a in swaps:
        raise Exception(f"{a} already in swaps")
    if b in swaps:
        raise Exception(f"{b} already in swaps")
    return swaps if a == b else (swaps | { a: b, b: a })

# Return solution to puzzle (sorted swapped outputs), or None if
# we reach a bad end (too many swaps, impossible swaps, etc).
def go(step, swaps, carry=None, local_sum=None, local_both=None, local_what=None):
    if len(swaps) > 8:
        return None

    if step < 2:
        bit = 0
        substep = step
    else:
        bit = (step - 2) // 5 + 1
        substep = (step - 2) % 5

    #print("go", step, "bit", bit, "substep", substep, "swaps", swaps)

    xvar = var_of("x", bit)
    yvar = var_of("y", bit)
    zvar = var_of("z", bit)

    if bit == 45 and substep == 0:
        if swaps.get(carry, carry) == zvar:
            return ",".join(sorted(swaps))
        else:
            return None

    if bit == 0:
        if substep == 0:
            output_gate = get_gate(xvar, "XOR", yvar, swaps)
            if output_gate == zvar:
                return go(step + 1, swaps)
            if output_gate in swaps:
                return None
            for other_bit in range(46):
                if other_bit != bit:
                    other = var_of("z", other_bit)
                    if other not in swaps:
                        solution = go(step + 1, with_swap(swaps, zvar, other))
                        if solution is not None:
                            return solution
            return None
        else:
            carry_gate = get_gate(xvar, "AND", yvar)

            for other in [carry_gate] + list(GATES):
                solution = go(step + 1, with_swap(swaps, carry_gate, other), carry=other)
                if solution is not None:
                    return solution
            return None
    else:
        if substep == 0:
            # x01 XOR y01 -> local_sum_01
            local_sum = get_gate(xvar, "XOR", yvar, swaps)
            solution = go(step + 1, swaps, local_sum=local_sum, carry=carry)
            if solution is not None:
                return solution
            if local_sum not in swaps:
                for other in list(GATES):
                    #print("BACKTRACKING", bit, substep, other)
                    if other not in swaps:
                        solution = go(step + 1, with_swap(swaps, local_sum, other), local_sum=other, carry=carry)
                        if solution is not None:
                            return solution
            return None
        elif substep == 1:
            # local_sum_01 XOR carry_out_00 -> z01
            output_gate = get_gate(local_sum, "XOR", carry, swaps)
            if output_gate is None:
                return None
            if output_gate == zvar:
                return go(step + 1, swaps, local_sum=local_sum, carry=carry)
            if output_gate not in swaps and zvar not in swaps:
                #print("BACKTRACKING", bit, substep, zvar)
                solution = go(step + 1, with_swap(swaps, output_gate, zvar), local_sum=local_sum, carry=carry)
                if solution is not None:
                    return solution
            return None
        elif substep == 2:
            # local_sum_01 AND carry_out_00 -> local_what_01
            local_what = get_gate(local_sum, "AND", carry, swaps)
            if local_what is None:
                return None
            solution = go(step + 1, swaps, local_what=local_what)
            if solution is not None:
                return solution
            if local_what not in swaps:
                for other in list(GATES):
                    if other not in swaps:
                        #print("BACKTRACKING", bit, substep, other)
                        solution = go(step + 1, with_swap(swaps, local_what, other), local_what=other)
                        if solution is not None:
                            return solution
            return None
        elif substep == 3:
            # x01 AND y01 -> local_both_01
            local_both = get_gate(xvar, "AND", yvar, swaps)
            solution = go(step + 1, swaps, local_both=local_both, local_what=local_what)
            if solution is not None:
                return solution
            if local_both not in swaps:
                for other in list(GATES):
                    if other not in swaps:
                        #print("BACKTRACKING", bit, substep, other)
                        solution = go(step + 1, with_swap(swaps, local_both, other), local_both=other, local_what=local_what)
                        if solution is not None:
                            return solution
            return None
        elif substep == 4:
            # local_what_01 OR local_both_01 -> carry_out_01
            carry_out = get_gate(local_what, "OR", local_both, swaps)
            if carry_out is None:
                return None
            solution = go(step + 1, swaps, carry=carry_out)
            if solution is not None:
                return solution
            if carry_out not in swaps:
                for other in list(GATES):
                    if other not in swaps:
                        #print("BACKTRACKING", bit, substep, other)
                        solution = go(step + 1, with_swap(swaps, carry_out, other), carry=other)
                        if solution is not None:
                            return solution
            return None

def do_part(part):
    if part == 1:
        total = 0

        for i in count():
            value = evaluate(var_of("z", i))
            if value is None:
                break
            total |= value << i

        return total
    else:
        return go(0, {})

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

