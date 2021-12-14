
from collections import Counter

lines = [line.strip() for line in open("input-14.txt")]
template = lines[0]
subst = dict(line.split(" -> ") for line in lines[2:])

pairs = Counter(template[i: i + 2] for i in range(len(template) - 1))

for step in range(40):
    new_pairs = Counter()

    for pair, count in pairs.items():
        insert = subst[pair]
        new_pairs[pair[0] + insert] += count
        new_pairs[insert + pair[1]] += count

    pairs = new_pairs

counts = Counter()
for pair, count in pairs.items():
    counts[pair[0]] += count
counts[template[-1]] += 1

counts = list(counts.values())
print(max(counts) - min(counts))

