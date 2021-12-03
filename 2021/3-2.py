
lines = [list(map(int,list(line.strip()))) for line in open("input-3-test.txt")]
width = len(lines[0])

def keep(lines, more):
    for i in range(width):
        if len(lines) == 1:
            break

        total = sum(line[i] for line in lines)
        half = len(lines)/2
        bit = 1 if (total >= half) == more else 0

        lines = list(filter(lambda line: line[i] == bit, lines))

    if len(lines) == 1:
        return int("".join(map(str, lines[0])), 2)

    raise Exception("Didn't converge")

gamma = keep(lines, True)
epsilon = keep(lines, False)

print(gamma, epsilon, gamma*epsilon)



