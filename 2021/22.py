
# mv ~/Downloads/input.txt input-22.txt

class Range:
    def __init__(self, r1, r2):
        if r1 > r2:
            raise Exception("%d > %d in range" % (r1, r2))
        self.r1 = r1
        self.r2 = r2

    def size(self):
        return self.r2 - self.r1 + 1

    def is_overlap(self, o):
        return not (o.r2 < self.r1 or o.r1 > self.r2)

    def clip(self, o, d):
        if d == -1:
            r1 = self.r1
            r2 = min(self.r2, o.r1 - 1)
        elif d == 0:
            r1 = max(self.r1, o.r1)
            r2 = min(self.r2, o.r2)
        else:
            r1 = max(o.r2 + 1, self.r1)
            r2 = self.r2
        if r1 <= r2:
            return Range(r1, r2)
        else:
            return None

    def __repr__(self):
        return "%d..%d" % (self.r1, self.r2)

class Cuboid:
    def __init__(self, on, x, y, z):
        self.on = on
        self.x = x
        self.y = y
        self.z = z

    def size(self):
        return self.x.size()*self.y.size()*self.z.size()

    def remove(self, o):
        if not self.x.is_overlap(o.x) or not self.y.is_overlap(o.y) or not self.z.is_overlap(o.z):
            return [self]

        cs = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if dx != 0 or dy != 0 or dz != 0:
                        new_x = self.x.clip(o.x, dx)
                        new_y = self.y.clip(o.y, dy)
                        new_z = self.z.clip(o.z, dz)
                        if new_x is not None and new_y is not None and new_z is not None:
                            cs.append(Cuboid(self.on, new_x, new_y, new_z))

        return cs

    def __repr__(self):
        return "%s x=%s,y=%s,z=%s" % ("on" if self.on else "off", self.x, self.y, self.z)

lines = [line.strip() for line in open("input-22.txt")]

cuboids = []
for line in lines:
    p = line.split(" ")
    on = p[0] == "on"
    p = [s[2:] for s in p[1].split(",")]
    x1, x2 = list(map(int, p[0].split("..")))
    y1, y2 = list(map(int, p[1].split("..")))
    z1, z2 = list(map(int, p[2].split("..")))
    cuboids.append(Cuboid(on, Range(x1, x2), Range(y1, y2), Range(z1, z2)))

count = 0
for i in range(len(cuboids)):
    # print(i)
    if not cuboids[i].on:
        # print("    off")
        continue

    broken = [cuboids[i]]
    for j in range(i + 1, len(cuboids)):
        # print("    broken size: %d" % len(broken))
        new_broken = []
        for c in broken:
            new_c = c.remove(cuboids[j])
            new_broken.extend(new_c)
        broken = new_broken

    this_count = sum(c.size() for c in broken)
    # print("    count: %d" % this_count)
    count += this_count

print(count)
