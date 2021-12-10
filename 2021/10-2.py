
from itertools import *
from more_itertools import *

lines = [line.strip() for line in open("input-10.txt")]

scores = []
for line in lines:
    score = 0
    stack = []
    for ch in line:
        if ch == "(" or ch == "<" or ch == "{" or ch == "[":
            if ch == "(":
                stack.append(")")
            elif ch == "[":
                stack.append("]")
            elif ch == "{":
                stack.append("}")
            elif ch == "<":
                stack.append(">")
        else:
            exp = stack.pop()
            if exp == ch:
                pass
            else:
                # print("found " + ch + " instead of " + exp)
                break
    else:
        while len(stack) > 0:
            ch = stack.pop()
            score *= 5
            if ch == ")":
                score += 1
            elif ch == "]":
                score += 2
            elif ch == "}":
                score += 3
            elif ch == ">":
                score += 4
            else:
                raise Exception("unexpected close " + ch)
            line = line + ch
        print(line)
        scores.append(score)

scores.sort()
print(scores[len(scores)//2])


