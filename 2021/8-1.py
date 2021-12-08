
from itertools import permutations

digits = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]

all_perm = list("".join(word) for word in permutations("abcdefg"))

def is_valid_perm(perm, inputs):
    for input in inputs:
        new_input = "".join(sorted(perm[ord(letter) - ord("a")] for letter in input))
        if new_input not in digits:
            return False

    return True

total = 0
for line in open("input-8.txt"):
    parts = line.split("|")
    inputs = parts[0].strip().split()
    outputs = parts[1].strip().split()

    for perm in all_perm:
        if is_valid_perm(perm, inputs):
            num = 0
            for output in outputs:
                new_output = "".join(sorted(perm[ord(letter) - ord("a")] for letter in output))
                index = digits.index(new_output)
                num = num*10 + index
            total += num
            break

print(total)




