
import time
from intcode import IntcodeLists, parse_mem

data = open("input-17.txt").read()
MEM = parse_mem(data)

CHAR_TO_DIR = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}
DIR_TO_CHAR = dict((b, a) for (a, b) in CHAR_TO_DIR.items())

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def left(dir):
    return dir[1], -dir[0]

def right(dir):
    return -dir[1], dir[0]

def print_tiles(tiles, w, h, robot):
    for y in range(h):
        s = ""
        for x in range(w):
            p = x,y
            if robot[0] == p:
                s += DIR_TO_CHAR[robot[1]]
            elif p in tiles:
                s += "#"
            else:
                s += "."
        print(s)

def check_if_works(moves, a_len, b_len, c_len):
    main_routine = []

    def append(x, letter):
        nonlocal moves, main_routine
        main_routine.append(letter)
        moves = moves[len(x):]

    def moves_start_with(prefix):
        nonlocal moves
        return moves[:len(prefix)] == prefix

    a = moves[:a_len]
    b = None
    c = None

    while True:
        if not moves:
            break
        elif moves_start_with(a):
            append(a, "A")
        elif b is not None and moves_start_with(b):
            append(b, "B")
        elif c is not None and moves_start_with(c):
            append(c, "C")
        elif b is None:
            b = moves[:b_len]
        elif c is None:
            c = moves[:c_len]
        else:
            return None

    s = ",".join(main_routine)
    if len(s) > 20:
        return None

    return main_routine, a, b, c

def decode_grid(outputs):
    grid = "".join(chr(ch) for ch in outputs).strip().split("\n")
    w = len(grid[0])
    h = len(grid)

    # Map from (x,y) to non-space char.
    tiles = set()
    robot = None
    for y in range(0, h):
        for x in range(0, w):
            ch = grid[y][x]
            if ch == "#":
                tiles.add( (x,y) )
            d = CHAR_TO_DIR.get(ch)
            if d is not None:
                robot = (x, y), d
                tiles.add( (x,y) )

    return tiles, w, h, robot

def make_full_list_of_moves(tiles, w, h, robot):
    moves = []
    p, d = robot
    while True:
        np = add(p, d)
        if np in tiles:
            if not moves or isinstance(moves[-1], str):
                moves.append(0)
            moves[-1] += 1
            p = np
        else:
            nd = left(d)
            np = add(p, nd)
            if np in tiles:
                moves.append("L")
                d = nd
            else:
                nd = right(d)
                np = add(p, nd)
                if np in tiles:
                    moves.append("R")
                    d = nd
                else:
                    break

    # Convert ints to strings.
    return [str(x) for x in moves]

def find_working_breakdown(moves):
    # Try every combination of function lengths (that fit).
    for a_len in range(2, 9, 2):
        for b_len in range(2, 9, 2):
            for c_len in range(2, 9, 2):
                solution = check_if_works(moves, a_len, b_len, c_len)
                if solution is not None:
                    return solution

    raise Exception("No solutions")

def do_part(part):
    ascii = IntcodeLists(MEM, [])
    outputs = ascii.run()
    tiles, w, h, robot = decode_grid(outputs)
    #print_tiles(tiles, w, h, robot)

    if part == 1:
        total = 0
        for x in range(0, w):
            for y in range(0, h):
                if (x,y) in tiles and \
                        (x,y - 1) in tiles and \
                        (x,y + 1) in tiles and \
                        (x - 1,y) in tiles and \
                        (x + 1,y) in tiles:

                    total += x*y
        return total
    else:
        moves = make_full_list_of_moves(tiles, w, h, robot)
        main_routine, a, b, c = find_working_breakdown(moves)

        input_string = ",".join(main_routine) + "\n" + \
                ",".join(a) + "\n" + \
                ",".join(b) + "\n" + \
                ",".join(c) + "\n" + \
                "n" + "\n"
        inputs = [ord(ch) for ch in input_string]
        ascii = IntcodeLists([2] + MEM[1:], inputs)
        outputs = ascii.run()
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
