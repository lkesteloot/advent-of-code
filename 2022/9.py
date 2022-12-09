
lines = [line.strip() for line in open("input-9-test2.txt")]
lines = [line.strip() for line in open("input-9.txt")]
# matrix = [list(map(int, list(line))) for line in lines]

SIZE = 10
rope = [(0,0)]*SIZE

visited = set()  # (x,y)

visited.add(rope[SIZE - 1])

for line in lines:
    dir, dist = line.split(" ")
    dist = int(dist)

    for i in range(dist):
        if False:
            for y in range(5, -1, -1):
                s = ""
                for x in range(6):
                    for q in range(SIZE):
                        if rope[q] == (x,y):
                            if q == 0:
                                s += "H"
                            else:
                                s += str(q)
                            break
                    else:
                        s += "."
                print(s)
        if dir == "U":
            rope[0] = (rope[0][0], rope[0][1] + 1)
        elif dir == "D":
            rope[0] = (rope[0][0], rope[0][1] - 1)
        elif dir == "L":
            rope[0] = (rope[0][0] - 1, rope[0][1])
        elif dir == "R":
            rope[0] = (rope[0][0] + 1, rope[0][1])
        else:
            raise Error()

        for q in range(0, SIZE - 1):
            dx = rope[q][0] - rope[q + 1][0]
            dy = rope[q][1] - rope[q + 1][1]
            if abs(dx) <= 1 and abs(dy) <= 1:
                pass
            else:
                if dx != 0: dx = dx//abs(dx)
                if dy != 0: dy = dy//abs(dy)
                rope[q + 1] = (rope[q + 1][0] + dx, rope[q + 1][1] + dy)
                if q == SIZE - 2:
                    visited.add(rope[q + 1])

print(len(visited))

