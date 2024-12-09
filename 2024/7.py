
lines = open("input-7-test.txt").read().splitlines()
lines = open("input-7.txt").read().splitlines()

def concat(a, b):
    return int(str(a) + str(b))

def matches(solution, accum, values, include_concat):
    if not values:
        return accum == solution

    if accum > solution:
        return False

    first, *rest = values
    return matches(solution, accum + first, rest, include_concat) or \
        matches(solution, accum * first, rest, include_concat) or \
        (include_concat and matches(solution, concat(accum, first), rest, include_concat))

def do_part(part):
    total = 0

    for line in lines:
        solution, values = line.split(": ")
        solution = int(solution)

        values = list(map(int, values.split(" ")))

        first, *rest = values
        if matches(solution, first, rest, part == 2):
            total += solution

    print(f"Part {part}: {total}")

do_part(1)
do_part(2)
