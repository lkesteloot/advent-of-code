

hor = list(map(int, open("input-7.txt").read().strip().split(",")))

def fuel(dx):
    dx = abs(dx)
    return dx*(dx + 1)/2

print(min(sum(fuel(pos - h) for h in hor) for pos in range(min(hor), max(hor) + 1)))

