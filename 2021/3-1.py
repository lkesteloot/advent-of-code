

lines = [list(map(int,list(line.strip()))) for line in open("input-3.txt")]
count = len(lines)
half = count // 2

sums = lines[0]

for i in range(1, count):
    for j in range(len(sums)):
        sums[j] += lines[i][j]

print(sums, count)

gamma = int("".join(map(lambda x: "1" if x > half else "0", sums)), 2)
epsilon = int("".join(map(lambda x: "1" if x < half else "0", sums)), 2)

print(gamma, epsilon, gamma*epsilon)

