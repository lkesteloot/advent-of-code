
lines = [line.strip() for line in open("input-25.txt")]
matrix = [list(line) for line in lines]
WIDTH = len(matrix[0])
HEIGHT = len(matrix)

def make_step(m, ch, dx, dy):
    can_move = [[False]*WIDTH for i in range(HEIGHT)]

    can_move_any = False
    for y in range(HEIGHT):
        new_y = (y + dy) % HEIGHT
        for x in range(WIDTH):
            new_x = (x + dx) % WIDTH
            if m[y][x] == ch and m[new_y][new_x] == ".":
                can_move[y][x] = True
                can_move_any = True

    if not can_move_any:
        return False

    for y in range(HEIGHT):
        new_y = (y + dy) % HEIGHT
        for x in range(WIDTH):
            new_x = (x + dx) % WIDTH
            if can_move[y][x]:
                m[new_y][new_x] = m[y][x]
                m[y][x] = "."

    return True

def print_matrix(m):
    for line in m:
        print("".join(line))
    print()

count = 0
while True:
    print("Trying step", count)
    #print_matrix(matrix)
    moved_h = make_step(matrix, ">", 1, 0)
    moved_v = make_step(matrix, "v", 0, 1)

    count += 1

    if not moved_h and not moved_v:
        print("Can't move at step", count)
        break

