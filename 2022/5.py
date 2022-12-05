
#lines = [line for line in open("input-5-test.txt")]
lines = [line for line in open("input-5.txt")]

stacks = [""] * 9

mode = 0
for line in lines:
    if mode == 0:
        if "[" not in line:
            stacks = [s.strip() for s in stacks]
            mode = 1
        else:
            for i in range(1, len(line), 4):
                stacks[(i - 1)//4] += line[i]
    elif mode == 1:
        mode = 2
    else:
        parts = line.split(" ")
        count = int(parts[1])
        f = int(parts[3]) - 1
        t = int(parts[5]) - 1
        print(count, f, t)

        ch = stacks[f][:count]
        stacks[f] = stacks[f][count:]
        stacks[t] = ch + stacks[t]

print("".join([s[0] for s in stacks]))

