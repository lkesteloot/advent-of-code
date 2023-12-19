
import re
import math

part2 = True

lines = open("input-19.txt").read()

workflows, parts = lines.split("\n\n")
workflows = workflows.split("\n")
parts = parts.strip().split("\n")

# s>2770:qs
def parse_rule(rule):
    parts = rule.split(":")
    if len(parts) == 1:
        return (True, parts[0])
    else:
        var, sym, value = re.findall(r'[a-z]|[<>]|[0-9]+', parts[0])
        return (var, sym, int(value)), parts[1]

# qqz{s>2770:qs,m<1801:hdj,R}
def parse_workflow(workflow):
    name, rules = workflow.split("{")
    rules = [parse_rule(rule) for rule in rules.rstrip("}").split(",")]

    return (name, rules)

# {x=2127,m=1623,a=2188,s=1013}
def parse_parts(part):
    categories = [category.split("=") for category in part.strip("{}").split(",")]
    return {var: int(value) for var, value in categories}

workflows = dict(parse_workflow(workflow) for workflow in workflows)
parts = [parse_parts(part) for part in parts]

def matches(part, step):
    if step == True:
        return True
    return part[step[0]] < step[2] if step[1] == "<" else part[step[0]] > step[2]

def accepted(part):
    workflow_name = "in"
    while True:
        workflow = workflows[workflow_name]
        for step in workflow:
            if matches(part, step[0]):
                if step[1] == "R":
                    return False
                if step[1] == "A":
                    return True
                workflow_name = step[1]
                break

def count(workflow_name, opts):
    if workflow_name == "R":
        return 0
    if workflow_name == "A":
        return math.prod(high - low + 1 for low, high in opts.values())

    workflow = workflows[workflow_name]

    total = 0
    for rule in workflow:
        if rule[0] == True:
            total += count(rule[1], opts)
            break

        var, sym, value = rule[0]
        low, high = opts[var]
        if sym == "<":
            yes_low = low
            yes_high = value - 1
            no_low = value
            no_high = high
        else:
            yes_low = value + 1
            yes_high = high
            no_low = low
            no_high = value

        if yes_low <= yes_high:
            total += count(rule[1], opts | {var: (yes_low, yes_high)})
        if no_low > no_high:
            break
        opts = opts | {var: (no_low, no_high)}
    return total

if part2:
    start_range = 1,4000
    print(count("in", dict(x=start_range, m=start_range, a=start_range, s=start_range)))
else:
    print(sum(sum(part.values()) for part in parts if accepted(part)))
