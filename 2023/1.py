
lines = [line.strip() for line in open("input-1.txt")]

digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def fix(line):
    first = None
    last = None
    for i, ch in enumerate(line):
        dd = None
        for j, d in enumerate(digits):
            if line[i:].startswith(d):
                dd = j + 1
        if ch.isdigit():
            dd = int(ch)
        if dd is not None and first is None:
            first = dd
        if dd is not None:
            last = dd
    return first*10 + last

print(sum(fix(line) for line in lines))

