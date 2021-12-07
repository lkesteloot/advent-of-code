
contents = open("input-6.txt").read().strip()
ages = map(int, contents.split(","))

age_count = [0]*10

for age in ages:
    age_count[age] += 1

for i in range(256):
    new_fish = age_count.pop(0)
    age_count.append(0)
    age_count[6] += new_fish
    age_count[8] += new_fish

print(sum(age_count))

