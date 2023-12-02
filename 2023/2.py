
from collections import defaultdict

lines = [line.strip() for line in open("input-2.txt")]

total = 0
for line in lines:
    game, rolls = line.split(": ")
    game_number = int(game.split(" ")[1])
    max_count = defaultdict(int)
    for roll in rolls.split("; "):
        dice = roll.split(", ")
        for die in dice:
            count, color = die.split(" ")
            max_count[color] = max(int(count), max_count[color])
    total += max_count["red"] * max_count["green"] * max_count["blue"]

print(total)
