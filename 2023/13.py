
part2 = True

patterns = open("input-13.txt").read().split("\n\n")

def transpose(lines):
    width = len(lines[0])
    height = len(lines)
    return ["".join(lines[j][i] for j in range(height)) for i in range(width)]

def hamming_distance(a, b):
    return sum(a[i] != b[i] for i in range(len(a)))

def find_mirror(lines):
    width = len(lines[0])
    revlines = [line[::-1] for line in lines]
    for i in range(1, width - 1):
        if i <= width/2:
            diff = sum(hamming_distance(line[:i], line[i:2*i][::-1]) for line in lines)
            if diff == int(part2):
                return i
        if i < width/2:
            diff = sum(hamming_distance(line[:i], line[i:2*i][::-1]) for line in revlines)
            if diff == int(part2):
                return width - i
    return 0

total = 0
for pattern in patterns:
    lines = pattern.strip().split("\n")
    col = find_mirror(lines)
    row = find_mirror(transpose(lines))
    total += row*100 + col
print(total)

