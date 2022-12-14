
lines = [line.strip() for line in open("input-14-test.txt")]
lines = [line.strip() for line in open("input-14.txt")]

rock = set() # (x,y)

for line in lines:
    points = line.split(" -> ")
    px, py = None, None
    for point in points:
        nx, ny = map(int, point.split(","))
        if px is not None:
            x = px
            y = py
            if x == nx:
                if y >= ny:
                    while y >= ny:
                        rock.add((x,y))
                        y -= 1
                elif y <= ny:
                    while y <= ny:
                        rock.add((x,y))
                        y += 1
            else:
                if x >= nx:
                    while x >= nx:
                        rock.add((x,y))
                        x -= 1
                elif x <= nx:
                    while x <= nx:
                        rock.add((x,y))
                        x += 1
        px = nx
        py = ny

max_y = 0
for x, y in rock:
    max_y = max(max_y, y)
print("max_y", max_y)
floor = max_y + 2


sand = set()
count = 0
all_done = False
while not all_done:
    x, y = 500, 0

    while True:
        if (x, y + 1) not in rock and y + 1 != floor:
            y += 1
        elif (x - 1, y + 1) not in rock and y + 1 != floor:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in rock and y + 1 != floor:
            x += 1
            y += 1
        else:
            count += 1
            if (x, y) == (500, 0):
                all_done = True
                break
            sand.add((x, y))
            rock.add((x, y))
            break


for y in range(0, 10):
    s = ""
    for x in range(494, 504):
        if (x, y) in sand:
            s += "o"
        elif (x, y) in rock:
            s += "#"
        else:
            s += "."
    print(s)
print("count", count)
