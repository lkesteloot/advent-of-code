
lines = open("input-15.txt").read().strip()

def myhash(s):
    x = 0
    for ch in s:
        x = (x + ord(ch))*17 % 256
    return x

# (label, power)
boxes = [[] for i in range(256)]

parts = lines.split(",")
for part in parts:
    if "=" in part:
        label, power = part.split("=")
        boxnum = myhash(label)
        power = int(power)
        box = boxes[boxnum]
        for i in range(len(box)):
            if box[i][0] == label:
                box[i] = label, power
                break
        else:
            box.append( (label, power) )
    else:
        label = part.strip("-")
        boxnum = myhash(label)
        box = boxes[boxnum]
        for i in range(len(box)):
            if box[i][0] == label:
                box.pop(i)
                break

print(sum(sum((i + 1) * (j + 1) * power
              for j, (_, power) in enumerate(box))
          for i, box in enumerate(boxes)))
