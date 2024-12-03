
import re

WITHOUT_CONDITIONALS = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
WITH_CONDITIONALS = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")

data = open("input-3-test.txt").read()
data = open("input-3.txt").read()

def do_part(part):
    pattern = WITH_CONDITIONALS if part == 2 else WITHOUT_CONDITIONALS
    total = 0
    enabled = True
    pos = 0

    while m := pattern.search(data, pos):
        if m[0] == "don't()":
            enabled = False
        elif m[0] == "do()":
            enabled = True
        elif enabled:
            total += int(m[1]) * int(m[2])
        pos = m.start() + 1

    print(f"Part {part}: {total}")

do_part(1)
do_part(2)
