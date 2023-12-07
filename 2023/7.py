
from collections import Counter

CARDS = "J23456789TQKA"

lines = open("input-7.txt").read().splitlines()

def process_hand(h):
    h = tuple(CARDS.index(c) for c in h)

    j = 0
    cs = Counter()
    for c in h:
        if c == 0:
            j += 1
        else:
            cs[c] += 1

    cs = sorted(cs.values(), reverse=True)

    if len(cs) == 0:
        cs = [j]
    else:
        cs[0] += j

    if cs[0] == 5:
        p = 6
    elif cs[0] == 4:
        p = 5
    elif cs[0] == 3 and cs[1] == 2:
        p = 4
    elif cs[0] == 3:
        p = 3
    elif cs[0] == 2 and cs[1] == 2:
        p = 2
    elif cs[0] == 2:
        p = 1
    else:
        p = 0

    return p, h

lines = [line.split() for line in lines]
lines = [(process_hand(h), int(b)) for h, b in lines]
lines.sort()

print(sum((i + 1)*b for i, (h, b) in enumerate(lines)))
