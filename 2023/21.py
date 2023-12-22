
import math

lines = open("input-21.txt").read().splitlines()

width = len(lines[0])
height = len(lines)
tiles = {(x, y): lines[y][x] for y in range(height) for x in range(width)}

N = 26501365
#N = 65 + 131*2
#N = 65 + 131*1
#N = 65 + 131*0

hashes = {(x, y) for (x, y), ch in tiles.items() if ch == "#"}
inside_hashes = {p for p in hashes if abs(p[0] - 65) + abs(p[1] - 65) <= 65}
outside_hashes = hashes - inside_hashes
print(f"{len(hashes)=}, {len(inside_hashes)=}, {len(outside_hashes)=}")
odd_inside_hashes = len({p for p in inside_hashes if sum(p) % 2 == 1})
odd_outside_hashes = len({p for p in outside_hashes if sum(p) % 2 == 1}) + 3 # trapped cells
even_inside_hashes = len({p for p in inside_hashes if sum(p) % 2 == 0}) + 1 # trapped cells
even_outside_hashes = len({p for p in outside_hashes if sum(p) % 2 == 0})
print(f"{odd_inside_hashes=}, {odd_outside_hashes=}, {even_inside_hashes=}, {even_outside_hashes=}")

total_O = (N + 1)**2
print(f"{total_O=}")

megasteps = (N - 65) // 131
megatiles = (megasteps*2 + 1)**2

wholes = math.ceil(megatiles/2)
if megasteps % 2 == 0:
    odds = (megasteps + 1)**2
    evens = megasteps**2
else:
    odds = megasteps**2
    evens = (megasteps + 1)**2
assert odds + evens == wholes
splits = math.floor(megatiles/2)
print(f"{odds=}, {evens=}, {splits=}")

odds *= odd_inside_hashes
evens *= even_inside_hashes
splits = splits*(odd_outside_hashes + even_outside_hashes)//2
total = odds + evens + splits
print(f"{odds=}, {evens=}, {splits=}, {total=}")
print("final", total_O - total)

