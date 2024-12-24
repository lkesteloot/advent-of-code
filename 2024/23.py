
import time
from collections import defaultdict

lines = open("input-23-test.txt").read().splitlines()
lines = open("input-23.txt").read().splitlines()

CONNECTIONS = [line.split("-") for line in lines]
NEIGHBORS = defaultdict(set)
for a, b in CONNECTIONS:
    NEIGHBORS[a].add(b)
    NEIGHBORS[b].add(a)

# Bron-Kerbosch algorithm with pivot.
def find_all_cliques(P, R=set(), X=set()):
    if not P and not X:
        yield ",".join(sorted(R))
    else:
        u = (P | X).pop()
        for v in P - NEIGHBORS[u]:
            yield from find_all_cliques(P & NEIGHBORS[v], R | {v}, X & NEIGHBORS[v])
            P = P - {v}
            X = X | {v}

def do_part(part):
    if part == 1:
        sets3 = set()
        for a in NEIGHBORS:
            for b in NEIGHBORS[a]:
                for c in NEIGHBORS[a] & NEIGHBORS[b]:
                    if a.startswith("t") or b.startswith("t") or c.startswith("t"):
                        sets3.add(",".join(sorted([a,b,c])))

        return len(sets3)
    else:
        _, best_clique = max((len(clique), clique)
                             for clique in find_all_cliques(NEIGHBORS.keys()))
        return best_clique

def main():
    for part in [1, 2]:
        before = time.perf_counter()
        answer = do_part(part)
        after = time.perf_counter()
        elapsed = round((after - before)*1_000_000)
        unit = "µs"
        if elapsed >= 1000:
            elapsed //= 1000
            unit = "ms"
        print(f"Part {part}: {answer} ({elapsed:,} {unit})")

main()
