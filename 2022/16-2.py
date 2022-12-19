
import re
import collections

lines = [line.strip() for line in open("input-16-test.txt")]
#lines = [line.strip() for line in open("input-16.txt")]

class Valve:
    def __init__(self, name, flow, neighbors):
        self.name = name
        self.flow = flow
        self.neighbors = neighbors

aa = None
vs = {}
for line in lines:
    # Valve HH has flow rate=22; tunnel leads to valve GG
    name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
    v = Valve(name, int(flow), neighbors)
    if name == "AA":
        aa = v
    vs[name] = v

def get_dist(start_name):
    q = collections.deque([(start_name, 0)])
    d = {}
    while q:
        name, dist = q.popleft()
        neighbors = vs[name].neighbors
        for n in neighbors:
            if n not in d:
                d[n] = dist + 1
                q.append((n, dist + 1))

    del d[start_name]
    d = {n: d for n, d in d.items() if vs[n].flow > 0}

    return d

# Precompute distance to every other flowable node.
dists = {}
for name in vs:
    dists[name] = get_dist(name)

def get_pressure(names, opened, time_left, other_left):
    if time_left <= 2:
        return 0

    # Working on the first person.
    name = names[0]

    pressure = 0

    for new_name, dist in dists[name].items():
        if new_name not in opened and dist + 1 < time_left:
            opened.add(new_name)
            new_pressure = (time_left - dist - 1)*vs[new_name].flow
            new_time_left = time_left - dist - 1
            new_other_left = other_left - dist - 1
            if new_other_left >= 0:
                new_names = [new_name, names[1]]
            else:
                new_names = [names[1], new_name]
                new_other_left = -new_other_left
                new_time_left += new_other_left

            p = new_pressure + get_pressure(new_names, opened, new_time_left, new_other_left)
            if p > pressure:
                pressure = p
            opened.remove(new_name)

    return pressure

#pressure = get_pressure([aa.name, aa.name], set(), 30, 100)
pressure = get_pressure([aa.name, aa.name], set(), 26, 0)
print(pressure)

