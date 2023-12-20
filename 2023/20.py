
import math
from collections import Counter, defaultdict

part2 = True

def load(filename):
    lines = open(filename).read().splitlines()

    # name -> (type, (outputs,))
    devs = {}
    # name ->
    #    %: True for high, False for low.
    #    &: Map from input to remembered value.
    state = {}

    for line in lines:
        left, right = line.split(" -> ")
        outputs = right.split(", ")
        if left == "broadcaster":
            devtype = "B"
            name = left
        else:
            devtype = left[0]
            name = left[1:]
        devs[name] = devtype, outputs
        if devtype == "%":
            state[name] = False

    # name -> [inputs to name]
    inputs = defaultdict(list)
    for name, (devtype, outputs) in devs.items():
        for output in outputs:
            inputs[output].append(name)

    for name, (devtype, outputs) in devs.items():
        if devtype == "&":
            state[name] = dict((input, False) for input in inputs[name])

    return devs, state

def press_button(devs, state, counts=None):
    # name, source, high/low
    pulses = [("broadcaster", "button", False)]

    rx_pressed = False
    while pulses:
        name, source, pulse_value = pulses.pop(0)
        if name == "rx" and not pulse_value:
            rx_pressed = True
        if counts is not None:
            counts[pulse_value] += 1
        if name in devs:
            devtype, outputs = devs[name]
            if devtype == "B":
                for output in outputs:
                    pulses.append( (output, name, pulse_value) )
            elif devtype == "%":
                if not pulse_value:
                    new_state = not state[name]
                    state[name] = new_state
                    for output in outputs:
                        pulses.append( (output, name, new_state) )
            elif devtype == "&":
                inputs = state[name]
                inputs[source] = pulse_value
                all_high = all(inputs.values())
                for output in outputs:
                    pulses.append( (output, name, not all_high) )

    return rx_pressed

if part2:
    counts = []
    for i in range(1, 5):
        devs, state = load(f"input-20-{i}.txt")
        presses = 0
        rx_pressed = False
        while not rx_pressed:
            rx_pressed = press_button(devs, state)
            presses += 1
        counts.append(presses)
    print(math.lcm(*counts))
else:
    devs, state = load("input-20.txt")
    counts = Counter()
    for i in range(1000):
        press_button(devs, state, counts)

    print(counts[False] * counts[True])
