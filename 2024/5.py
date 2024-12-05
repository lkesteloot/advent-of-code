
from functools import cmp_to_key

data = open("input-5-test.txt").read()
data = open("input-5.txt").read()

rules, updates = data.strip().split("\n\n")
is_before = set(rules.split("\n"))

def is_before_cmp(a,b):
    if a + "|" + b in is_before:
        return -1;
    if b + "|" + a in is_before:
        return 1;
    return 0

def do_part(part):
    total = 0

    for update in updates.split("\n"):
        parts = update.split(",")
        sorted_parts = sorted(parts, key=cmp_to_key(is_before_cmp))
        if (part == 1) == (sorted_parts == parts):
            total += int(sorted_parts[len(sorted_parts)//2])

    print(f"Part {part}: {total}")

do_part(1)
do_part(2)
