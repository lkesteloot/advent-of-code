
lines = [line.strip() for line in open("input-12.txt")]

caves = []
conn = {}

for line in lines:
    a, b = line.split("-")
    if a not in caves: caves.append(a)
    if b not in caves: caves.append(b)
    conn[a + "-" + b] = True
    conn[b + "-" + a] = True

paths = []
def go(path, small_cave):
    here = path[-1]
    if here == "end":
        paths.append(",".join(path))
    else:
        for cave in caves:
            if conn.get(here + "-" + cave, False):
                is_large = cave.upper() == cave
                if is_large or cave not in path or (cave == small_cave and path.count(small_cave) < 2):
                    go(path + [cave], small_cave)

small_caves = list(cave for cave in caves if cave.upper() != cave and cave != "start" and cave != "end")
for small_cave in small_caves:
    go(["start"], small_cave)

print(len(set(paths)))



