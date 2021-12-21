
from collections import Counter

# world is (p1 position, p1 score, p2 position, p2 score)
worlds = Counter()
#worlds[(4, 0, 8, 0)] = 1
worlds[(8, 0, 7, 0)] = 1

counts = Counter()
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            s = i + j + k
            counts[s] += 1
# [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]

wins = [0, 0, 0]
t = 0  # or 2
while len(worlds) > 0:
    new_worlds = Counter()
    for world, count in worlds.items():
        for moves, num in counts.items():
            new_world = list(world)
            pos = new_world[t]
            pos = (pos - 1 + moves) % 10 + 1
            new_world[t] = pos
            new_world[t + 1] += pos
            new_world = tuple(new_world)
            new_worlds[new_world] += count*num
    worlds = new_worlds

    new_worlds = Counter()
    for world, count in worlds.items():
        if world[t + 1] >= 21:
            wins[t] += count
        else:
            new_worlds[world] += count
    worlds = new_worlds
    print(len(worlds))
    t = 2 - t

print(wins)
print(max(wins))

