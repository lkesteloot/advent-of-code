
from collections import Counter

CARDS = "J23456789TQKA"

lines = open("input-7.txt").read().splitlines()

def process_line(hand, bid):
    hand = tuple(CARDS.index(card) for card in hand)

    counts = Counter(hand)
    j = counts[0]
    counts[0] = 0

    power = sorted(counts.values(), reverse=True) or [0]
    power[0] += j

    return (power, hand), int(bid)

lines = sorted(process_line(*line.split()) for line in lines)

print(sum((i + 1)*bid for i, (_, bid) in enumerate(lines)))

