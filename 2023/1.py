
lines = [line.strip() for line in open("input-1.txt")]

WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def fix(line):
    digits = []
    for i, ch in enumerate(line):
        digit = None
        for j, word in enumerate(WORDS):
            if line[i:].startswith(word):
                digit = j
        if ch.isdigit():
            digit = int(ch)
        if digit is not None:
            digits.append(digit)
    return digits[0]*10 + digits[-1]

print(sum(fix(line) for line in lines))

