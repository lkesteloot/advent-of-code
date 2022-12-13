
from functools import cmp_to_key
import json

lines = [line.strip() for line in open("input-13-test.txt")]
lines = [line.strip() for line in open("input-13.txt")]

def in_order(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None
    if type(left) == int:
        return in_order([left], right)
    if type(right) == int:
        return in_order(left, [right])
    for i in range(min(len(left), len(right))):
        cmp = in_order(left[i], right[i])
        if cmp != None:
            return cmp
    if len(left) < len(right):
        return True
    if len(left) > len(right):
        return False
    return None

if False:
    s = 0
    for i in range(len(lines)//3):
        left = json.loads(lines[i*3])
        right = json.loads(lines[i*3 + 1])
        if in_order(left, right):
            s += i + 1
    print(s)
else:
    p = [json.loads(line) for line in lines if line != ""]
    d1 = [[2]]
    d2 = [[6]]
    p.append(d1)
    p.append(d2)
    p.sort(key=cmp_to_key(lambda a,b: -1 if in_order(a,b) else 1))
    p1 = None
    p2 = None
    for i in range(len(p)):
        if p[i] == d1: p1 = i + 1
        if p[i] == d2: p2 = i + 1
    print(p1*p2)

