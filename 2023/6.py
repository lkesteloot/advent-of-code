
import math

lines = open("input-6.txt").read().splitlines()

time = int(lines[0].replace(" ", "").split(":")[1])
distance = int(lines[1].replace(" ", "").split(":")[1])

A = 1
B = -time
C = distance

disc = math.sqrt(B*B - 4*A*C)

v1 = math.ceil((-B - disc)/(2*A))
v2 = math.floor((-B + disc)/(2*A))

print(v2 - v1 + 1)

