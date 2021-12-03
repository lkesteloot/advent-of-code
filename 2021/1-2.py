
values = [int(line) for line in open("input-1.txt")]

values1 = values[0:-2]
values2 = values[1:-1]
values3 = values[2:]

sums = [sum(parts) for parts in zip(values1, values2, values3)]

count = 0
for i in range(1, len(sums)):
    if sums[i] > sums[i - 1]:
        count += 1
print(count)

