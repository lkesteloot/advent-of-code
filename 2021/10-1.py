
from itertools import *
from more_itertools import *

lines = [line.strip() for line in open("input-10.txt")]

score = 0
for line in lines:
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
                print("found " + ch + " instead of " + exp)
                if ch == ")":
                    score += 3
                elif ch == "]":
                    score += 57
                elif ch == "}":
                    score += 1197
                elif ch == ">":
                    score += 25137
                else:
                    raise Exception("unexpected close " + ch)
                break
    else:
        print("line ok")

print(score)


