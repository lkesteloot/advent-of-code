
value = "target area: x=70..125, y=-159..-121"  # real input
#value = "target area: x=20..30, y=-10..-5"  # test

value = value[15:]
rangex, rangey = value.split(", y=")
rangex = tuple(map(int, rangex.split("..")))
rangey = tuple(map(int, rangey.split("..")))

def get_max_y(dx, dy):
    x = 0
    y = 0
    max_y = y
    while x <= rangex[1] and y >= rangey[0]:
        #print(x, y, dx, dy)
        x += dx
        y += dy
        if dx != 0:
            dx -= abs(dx)//dx
        dy -= 1

        max_y = max(max_y, y)
        if x >= rangex[0] and x <= rangex[1] and \
            y >= rangey[0] and y <= rangey[1]:

            #print("in range", x, y, dx, dy)
            return max_y

    return None

best_max_y = -9999
c = 0

for dy in range(-200, 1000):
    for dx in range(0, 200):
        m = get_max_y(dx, dy)
        if m is not None:
            c += 1
        if m is not None and m > best_max_y:
            best_max_y = m

print(c, best_max_y)
