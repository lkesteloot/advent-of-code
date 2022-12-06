
lines = [line.strip() for line in open("input-6.txt")]

count = 14
for line in lines:
    for i in range(count - 1, len(line)):
        s = set(line[i - (count - 1):i + 1])
        if len(s) == count:
            print(i + 1)
            break

