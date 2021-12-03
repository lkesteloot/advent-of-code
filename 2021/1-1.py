
values = [int(line) for line in open("input-1.txt")]

count = 0
for i in range(1, len(values)):
    if values[i] > values[i - 1]:
        count += 1
print(count)

