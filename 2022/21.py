
lines = [line.strip() for line in open("input-21-test.txt")]
lines = [line.strip() for line in open("input-21.txt")]

# name to either int or [name, op, name].
monkeys = {}

# name to monkey's parent. there is only one per monkey in input data.
parent = {}

# parse input and remember parent of each (if any).
for line in lines:
    name = line[:4]
    rhs = line[6:].split(" ")
    if len(rhs) == 1:
        rhs = int(rhs[0])
    else:
        parent[rhs[0]] = name
        parent[rhs[2]] = name
    monkeys[name] = rhs

# compute set of monkeys from humn (inclusive) to root (exclusive).
human_ancestors = set()
name = "humn"
while parent[name] != "root":
    human_ancestors.add(name)
    name = parent[name]
print("human_ancestors", human_ancestors)

# evaluate tree rooted at "name".
def evaluate(name):
    m = monkeys[name]
    if type(m) == int:
        return m
    a = evaluate(m[0])
    b = evaluate(m[2])
    if m[1] == "+":
        m = a + b
    elif m[1] == "-":
        m = a - b
    elif m[1] == "*":
        m = a * b
    elif m[1] == "/":
        m = a // b
    return m

# find value of "humn" that would get "name" to evalute to "target_value".
def find_human_value(name, target_value):
    if name == "humn":
        return target_value

    m = monkeys[name]
    if type(m) == int:
        # there can't be any integers on this side, it's all equations.
        raise Exception(name)

    if m[1] == "+":
        if m[0] in human_ancestors:
            other_value = evaluate(m[2])
            return find_human_value(m[0], target_value - other_value)
        else:
            other_value = evaluate(m[0])
            return find_human_value(m[2], target_value - other_value)
    elif m[1] == "-":
        if m[0] in human_ancestors:
            other_value = evaluate(m[2])
            return find_human_value(m[0], target_value + other_value)
        else:
            other_value = evaluate(m[0])
            return find_human_value(m[2], other_value - target_value)
    elif m[1] == "*":
        if m[0] in human_ancestors:
            other_value = evaluate(m[2])
            return find_human_value(m[0], target_value // other_value)
        else:
            other_value = evaluate(m[0])
            return find_human_value(m[2], target_value // other_value)
    elif m[1] == "/":
        if m[0] in human_ancestors:
            other_value = evaluate(m[2])
            return find_human_value(m[0], target_value * other_value)
        else:
            other_value = evaluate(m[0])
            return find_human_value(m[2], other_value // target_value)

root = monkeys["root"]

human_side = root[2] if root[2] in human_ancestors else root[0]
print("human_side", human_side)

non_human_side = root[0] if root[2] in human_ancestors else root[2]
print("non_human_side", non_human_side)

known_value = evaluate(non_human_side)
print("known_value", known_value)

human_value = find_human_value(human_side, known_value)
print("human_value", human_value)

