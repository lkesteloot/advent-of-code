
import time
from intcode import IntcodeLists, parse_mem

data = open("input-21.txt").read()
MEM = parse_mem(data)

# J = (!A or !B or !C) and D
# J = !(A and B and C) and D
PART_1_PROGRAM = """\
NOT A J
NOT J J
AND B J
AND C J
NOT J J
AND D J
WALK
"""

# You land 4 tiles after your jump command.
#
# Currently jumping here:
#
#      @
#    #####.#.#...#####
#       ABCDEFGHI
#
# Want to jump here:
#
#        @
#    #####.#.#...#####
#         ABCDEFGHI
#
#
# If E and H are both false, don't jump.

# So want all of:
#
#   A, B, or C are false
#   D is true
#   E or H are true
#
# J = !(A & B & C) & D & (E | H)
#

PART_2_PROGRAM = """\
NOT A J
NOT J J
AND B J
AND C J
NOT J J
AND D J
NOT E T
NOT T T
OR H T
AND T J
RUN
"""

def to_ascii(s):
    return map(ord, s)

def from_ascii(lst):
    return "".join(map(chr, lst))

def do_part(part):
    program = [PART_1_PROGRAM, PART_2_PROGRAM][part - 1]
    ic = IntcodeLists(MEM, to_ascii(program))
    outputs = ic.run()
    in_ascii = [ch for ch in outputs if ch < 256]
    not_in_ascii = [ch for ch in outputs if ch >= 256]
    if not_in_ascii:
        return not_in_ascii[0]
    else:
        print(from_ascii(in_ascii))

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
