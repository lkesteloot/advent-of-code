
lines = [line.strip() for line in open("input-5.txt")]
lines = [line.split(" -> ") for line in lines]
lines = [(
    tuple(map(int, start.split(","))),
    tuple(map(int,   end.split(",")))) for (start,end) in lines]

size = max(max(max(start), max(end)) for (start,end) in lines) + 1

grid = [[0]*size for i in range(size)]

for start, end in lines:
    if start[0] == end[0]:
        # vertical
        y1 = min(start[1], end[1])
        y2 = max(start[1], end[1])
        x = start[0]
        for y in range(y1, y2 + 1):
            grid[y][x] += 1
    elif start[1] == end[1]:
        # horizontal
        x1 = min(start[0], end[0])
        x2 = max(start[0], end[0])
        y = start[1]
        for x in range(x1, x2 + 1):
            grid[y][x] += 1
    else:
        # diagonal
        if start[0] > end[0]:
            start, end = end, start
        x1 = start[0]
        x2 = end[0]
        y = start[1]
        for x in range(x1, x2 + 1):
            grid[y][x] += 1
            if start[1] < end[1]:
                y += 1
            else:
                y -= 1

total = sum(sum(1 for cell in row if cell >= 2) for row in grid)
print(total)

