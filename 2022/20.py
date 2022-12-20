
lines = [line.strip() for line in open("input-20-test.txt")]
# lines = [line.strip() for line in open("input-20.txt")]

key = 811589153

class Int:
    def __init__(self, v):
        self.v = v

objs = []
final = []
zero = None
for line in lines:
    o = Int(int(line)*key)
    objs.append(o)
    final.append(o)
    if o.v == 0:
        zero = o
size = len(final)

for round in range(10):
    for i in range(size):
        o = objs[i]
        p1 = final.index(o)
        p2 = (p1 + o.v) % (size - 1)
        final.pop(p1)
        final.insert(p2, o)

p1 = final.index(zero)
print(
        final[(p1 + 1000) % size].v +
        final[(p1 + 2000) % size].v +
        final[(p1 + 3000) % size].v)

