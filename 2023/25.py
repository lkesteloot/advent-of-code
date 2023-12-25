
import networkx as nx

lines = open("input-25.txt").read().splitlines()

G = nx.Graph()
for line in lines:
    left, right = line.split(": ")
    right = right.split()

    for x in right:
        G.add_edge(left, x, weight=1)

cut_value, partition = nx.stoer_wagner(G)
a, b = partition
print(len(a)*len(b))

