
lines = [line.strip() for line in open("input-17-test.txt")]
lines = [line.strip() for line in open("input-17.txt")]

ROCKS = [
        [
            "####"
        ],
        [
            ".#.",
            "###",
            ".#.",
        ],
        [
            "..#",
            "..#",
            "###",
        ],
        [
            "#",
            "#",
            "#",
            "#",
        ],
        [
            "##",
            "##",
        ],
]

line = lines[0]
stack = []
inst_index = 0

def touches(stack, rock, x, y):
    for row in range(len(rock)):
        if y - row < len(stack):
            for col in range(len(rock[row])):
                if rock[row][col] == "#" and stack[y - row][x + col] == "#":
                    return True
    return False

def stamp(stack, row, x, y):
    while y >= len(stack):
        stack.append("       ")
    for row in range(len(rock)):
        c = list(stack[y - row])
        for col in range(len(rock[row])):
            if rock[row][col] == "#":
                if c[x + col] == "#":
                    raise Exception("problem at %d,%d" % (x + col, y - row))
                c[x + col] = "#"
        stack[y - row] = "".join(c)

def dump(stack):
    print()
    for row in reversed(stack):
        print("|" + row + "|")
    print("+-------+")

counts = []
for year in range(20220):
    rock_index = year % len(ROCKS)
    #print(rock_index, inst_index)
    if rock_index == 0:
        print("looped", year, len(stack), inst_index)
    rock = ROCKS[rock_index]
    width = len(rock[0])
    height = len(rock)
    x, y = 2, len(stack) + 2 + height

    while True:
        inst = line[inst_index]
        inst_index = (inst_index + 1) % len(line)
        if inst == "<":
            if x > 0 and not touches(stack, rock, x - 1, y):
                x -= 1
        if inst == ">":
            if x < 7 - width and not touches(stack, rock, x + 1, y):
                x += 1

        y -= 1
        if y + 1 < height or touches(stack, rock, x, y):
            y += 1
            #print(x, y)
            stamp(stack, rock, x, y)
            #dump(stack)
            break

"""
found a loop by hand:

looped 1350 2125 7730
looped 3065 4815 7730
looped 4780 7505 7730
looped 6495 10195 7730

c = 1000000000000
(c - 1350) // (3065 - 1350) * (4815 - 2125) + 2125

380 rocks at the end
add to 1350 = 1730
looped 1730 2751 10032
diff = 2751 - 2125 = 626

2151603493255 too high
2151603496945 too high
1568513118945 too low
1568513118945 + 626 = 1568513119571 = correct

"""
