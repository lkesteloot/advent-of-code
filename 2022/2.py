
lines = [line.strip() for line in open("input-2.txt")]

MAP = {
        "A": 0,
        "B": 1,
        "C": 2,
}

score = 0
for line in lines:
    theirs, outcome = line.split(" ")

    theirs = MAP[theirs]

    if outcome == "X":
        ours = (theirs + 2) % 3
    if outcome == "Y":
        ours = (theirs + 0) % 3
    if outcome == "Z":
        ours = (theirs + 1) % 3

    score += ours + 1

    if theirs == ours:
        score += 3
    elif ours == (theirs + 1) % 3:
        score += 6
    else:
        score += 0

print(score)

