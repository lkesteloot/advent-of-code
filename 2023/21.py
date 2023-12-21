
import math

lines = open("input-21.txt").read().splitlines()

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

width = len(lines[0])
height = len(lines)
tiles = {(x, y): lines[y][x] for y in range(height) for x in range(width)}

if True:
    N = 26501365
    #N = 65 + 131*2
    #N = 65 + 131*1
    #N = 65 + 131*0

    hashes = {(x, y) for (x, y), ch in tiles.items() if ch == "#"}
    inside_hashes = {p for p in hashes if abs(p[0] - 65) + abs(p[1] - 65) <= 65}
    outside_hashes = hashes - inside_hashes
    print(f"{len(hashes)=}, {len(inside_hashes)=}, {len(outside_hashes)=}")
    odd_inside_hashes = len({p for p in inside_hashes if sum(p) % 2 == 1}) + 0
    odd_outside_hashes = len({p for p in outside_hashes if sum(p) % 2 == 1}) + 3
    even_inside_hashes = len({p for p in inside_hashes if sum(p) % 2 == 0}) + 1
    even_outside_hashes = len({p for p in outside_hashes if sum(p) % 2 == 0})
    print(f"{odd_inside_hashes=}, {odd_outside_hashes=}, {even_inside_hashes=}, {even_outside_hashes=}")

    if False:
        for y in range(height):
            print("".join("1" if (x, y) in odd_inside_hashes else
                          "2" if (x, y) in even_inside_hashes else
                          "3" if (x, y) in odd_outside_hashes else
                          "4" if (x, y) in even_outside_hashes else
                          "." for x in range(width)))

    total_O = (N + 1)**2
    print(f"{total_O=}")

    megasteps = (N - 65) // 131
    megatiles = (megasteps*2 + 1)**2

    wholes = math.ceil(megatiles/2)
    if megasteps % 2 == 0:
        odds = (megasteps + 1)**2
        evens = megasteps**2
    else:
        odds = megasteps**2
        evens = (megasteps + 1)**2
    assert odds + evens == wholes
    splits = math.floor(megatiles/2)
    print(f"{odds=}, {evens=}, {splits=}")

    odds *= odd_inside_hashes
    evens *= even_inside_hashes
    splits = splits*(odd_outside_hashes + even_outside_hashes)//2
    total = odds + evens + splits
    print(f"{odds=}, {evens=}, {splits=}, {total=}")
    print("final", total_O - total)

else:

    def draw(plots):
        print("----------")
        for y in range(-height + 1, height*2):
            print("".join("O" if (x, y) in plots else tiles[x % width, y % height] for x in range(-width + 1, width*2)))

    twenty_five = 0
    eighty_one = 0
    FIRST = 65
    THEN = 131

    p = next(p for p, ch in tiles.items() if ch == "S")
    plots = {p}
    for i in range(1, FIRST + 0*THEN + 1):
        if i in [FIRST, FIRST + THEN, FIRST + THEN*2] and False:
            draw(plots)
        new_plots = set()
        for p in plots:
            for dx, dy in DIRS:
                new_p = p[0] + dx, p[1] + dy
                if tiles[new_p[0] % width, new_p[1] % height] in ".S":
                    new_plots.add(new_p)
        plots = new_plots
        if i == FIRST:
            inside = len(plots)
        if i == FIRST + 2*THEN:
            twenty_five = len(plots)
        if i == FIRST + 4*THEN:
            eighty_one = len(plots)
        print(i, len(plots))

