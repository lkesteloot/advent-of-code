
lines = [line.strip() for line in open("input-4.txt")]

fully = 0
overlap = 0

for line in lines:
    first, second = line.split(",")
    from1, to1 = map(int, first.split("-"))
    from2, to2 = map(int, second.split("-"))

    if (from2 >= from1 and to2 <= to1) or (from1 >= from2 and to1 <= to2):
        fully += 1

    if not (to2 < from1 or to1 < from2):
        overlap += 1

print(fully, overlap)

