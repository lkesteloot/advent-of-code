
# mv ~/Downloads/input.txt input-24.txt

import sys, re, time
from collections import defaultdict, Counter
from itertools import *
from functools import *
# https://more-itertools.readthedocs.io/en/stable/
from more_itertools import *
import numpy as np
# import scipy.signal

data = open("input-24-test.txt").read()
data = open("input-24.txt").read()
# width = len(lines[0])
# height = len(lines)
# matrix = [list(map(int, list(line))) for line in lines]
# name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
# grid = np.array([list(line) for line in lines])
# grid = np.pad(grid, 1, constant_values=-1)
# yxs = (yx for yx, ch in np.ndenumerate(grid) if is_symbol(ch))
# tiles = {(x, y): lines[y][x] for y in range(height) for x in range(width)}
# rolls = {(x, y) for y in range(height) for x in range(width) if lines[y][x] == "O"}
#    for m in re.finditer(r"[0-9]+", line):
#        begin, end = m.span()
#        value = int(m.group(0))

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

def add(p, d):
    return p[0] + d[0], p[1] + d[1]

def print_grid(grid):
    for row in grid:
        print("".join(str(tile) for tile in row))

# Returns value (0 or 1) and set of gates used in evaluation.
def evaluate(var):
    value = INITIAL.get(var)
    if value is not None:
        return value, set()

    gate = GATES.get(var)
    if gate is None:
        return None, None

    left, op, right = gate
    left, left_gates = evaluate(left)
    right, right_gates = evaluate(right)

    if op == "AND":
        value = int(left and right)
    elif op == "OR":
        value = int(left or right)
    elif op == "XOR":
        value = int(xor(left, right))
    else:
        raise Exception()

    return value, (left_gates | right_gates | {var})

def var_of(letter, number):
    return letter + "%02d" % number

def is_gate(gate, var1, op, var2):
    return gate[1] == op and \
            ((gate[0] == var1 and gate[2] == var2) or
             (gate[0] == var2 and gate[2] == var1))

def get_gate(var1, op, var2, swaps={}):
    gate = GATES_REV.get(sort_ops( (var1, op, var2) ))
    if gate is None:
        return None
        raise Exception()
        alts_for_var1 = []
        alts_for_var2 = []
        for ovar1, oop, ovar2 in GATES.values():
            if oop == op:
                if ovar1 == var1:
                    alts_for_var2.append(ovar2)
                if ovar2 == var1:
                    alts_for_var2.append(ovar1)
                if ovar1 == var2:
                    alts_for_var1.append(ovar2)
                if ovar2 == var2:
                    alts_for_var1.append(ovar1)
        if alts_for_var1 and not alts_for_var2:
            print("    ", f"Possible swap for {var1}: {alts_for_var1}")
        if alts_for_var2 and not alts_for_var1:
            print("    ", f"Possible swap for {var2}: {alts_for_var1}")
        if alts_for_var1 and alts_for_var2:
            print("    ", f"Possibly both are swapped")
        if not alts_for_var1 and not alts_for_var2:
            print("    ", f"No idea")
        raise Exception()

    return swaps.get(gate, gate)

def explain(var):
    gate = GATES.get(var)
    if gate is None:
        return var
    else:
        left, op, right = gate
        return "(" + explain(left) + " " + op + " " + explain(right) + ")"

def with_swap(swaps, a, b):
    if a in swaps:
        raise Exception(f"{a} already in swaps")
    if b in swaps:
        raise Exception(f"{b} already in swaps")
    return swaps if a == b else (swaps | { a: b, b: a })

best_bit = -1

# Return solution to puzzle (sorted swapped outputs), or None if
# we reach a bad end (too many swaps, impossible swaps, etc).
def go(step, swaps, carry=None, local_sum=None, local_both=None, local_what=None):
    global best_bit

    if len(swaps) > 8:
        return None

    if step < 2:
        bit = 0
        substep = step
    else:
        bit = (step - 2) // 5 + 1
        substep = (step - 2) % 5

    if bit > best_bit:
        print("Best bit", best_bit)
        best_bit = bit
    print("go", step, "bit", bit, "substep", substep, "swaps", swaps)

    xvar = var_of("x", bit)
    yvar = var_of("y", bit)
    zvar = var_of("z", bit)

    if bit == 45 and substep == 0:
        if swaps.get(carry, carry) == zvar:
            return ",".join(sorted(swaps))
        else:
            return None

    #if len(swaps) > 2:
    #    raise Exception()

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
                    print("BACKTRACKING", bit, substep, other)
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
                print("BACKTRACKING", bit, substep, zvar)
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
                        print("BACKTRACKING", bit, substep, other)
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
                        print("BACKTRACKING", bit, substep, other)
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
                        print("BACKTRACKING", bit, substep, other)
                        solution = go(step + 1, with_swap(swaps, carry_out, other), carry=other)
                        if solution is not None:
                            return solution
            return None

def do_part(part):
    if part == 1:
        total = 0

        for i in count():
            value, _ = evaluate(var_of("z", i))
            if value is None:
                break
            total |= value << i

        return total
    else:
        swaps = {}
        # swaps = with_swap(swaps, "qff", "qnw")
        # swaps = with_swap(swaps, "z16", "pbv")
        # swaps = with_swap(swaps, "z23", "qqp")
        # swaps = with_swap(swaps, "z36", "fbq")
        return go(0, swaps)

        # All possible things that could be swapped.
        all_gates = set(GATES)
        # The ones we know are fine.
        known_good = set()
        for i in range(46):
            print(i)

            xvar = var_of("x", i)
            yvar = var_of("y", i)
            zvar = var_of("z", i)

            # Check each adder.
            if i == 0:
                output_gate = get_gate(xvar, "XOR", yvar)
                carry_gate = get_gate(xvar, "AND", yvar)
                print("    ", output_gate, carry_gate)
            elif i == 45:
                output_gate = carry_gate
                print("    ", output_gate)
            else:
                while True:
                    # These will always succeed, but we don't know if the
                    # output values are right:
                    local_sum = get_gate(xvar, "XOR", yvar)
                    local_both = get_gate(xvar, "AND", yvar)

                    # These will fail if their inputs are bad:
                    try:
                        output_gate = get_gate(local_sum, "XOR", carry_gate)
                        local_what = get_gate(local_sum, "AND", carry_gate)
                    except:
                        # One or both input are bad.
                        options = []
                        for var1 in { local_sum } | (all_gates - known_good):
                            for var2 in ({ carry_gate } | (all_gates - known_good)) - { var1 }:
                                try:
                                    tentative_output_gate = get_gate(var1, "XOR", var2)
                                    get_gate(var1, "AND", var2)
                                    options.append( (var1, var2) )
                                except:
                                    # Keep trying
                                    pass
                        print(options)
                        return

                    # If both above pass, then these are good:
                    known_good |= {local_sum, carry_gate}

                    # If this works, then the inputs are good:
                    carry_gate = get_gate(local_both, "OR", local_what)
                    known_good |= {local_both, local_what}
                    break

                print("    ", local_sum, local_both, output_gate, local_what, carry_gate)

            if output_gate == zvar:
                known_good |= {output_gate}
            else:
                print(f"Output gate is wrong, {output_gate} should be {zvar}")

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

"""

There is 1 initial bit (z00), 44 middle bits (z01-z44), and one final carry bit (z45).

Adding module:

        Z = (X xor Y) xor IN
        OUT = (X and Y) or (IN and X) or (IN and Y)
        OUT = (X and Y) or (IN and (X xor Y))

        X Y IN  OUT Z
        0 0 0   0   0
        0 0 1   0   1
        0 1 0   0   1
        0 1 1   1   0
        1 0 0   0   1
        1 0 1   1   0
        1 1 0   1   0
        1 1 1   1   1

generic adder:

    x XOR y -> local_sum
    local_sum XOR carry -> z
    local_sum AND carry -> what
    x AND y -> both
    what OR both -> carry

bit 11 (qnw & qff):

    x11 XOR y11 -> qff   (*)
    ncw XOR qnw -> z11
    ncw AND qnw -> stw
    x11 AND y11 -> qnw   (*)
    qff OR stw -> wsv

bit 16 (z16 & pbv):

    x16 XOR y16 -> dfn
    dfn XOR qcr -> pbv   (*)
    dfn AND qcr -> mvp
    x16 AND y16 -> z16   (*)
    mvp OR pbv -> dbj

bit 23 (qqp & z23):

    x23 XOR y23 -> bcd
    cts XOR bcd -> qqp   (*)
    bcd AND cts -> jcd
    x23 AND y23 -> wdr
    wdr OR jcd -> z23    (*)

bit 36 (fbq & z36):

    y36 XOR x36 -> rbm
    jdd XOR rbm -> fbq   (*)
    jdd AND rbm -> z36   (*)
    x36 AND y36 -> rpw
    rpw OR fbq -> fhv

"""

