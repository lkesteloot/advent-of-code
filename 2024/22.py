
import time
import numpy as np

lines = open("input-22-test.txt").read().splitlines()
lines = open("input-22-test-2.txt").read().splitlines()
lines = open("input-22.txt").read().splitlines()

INITIAL = np.array(lines, int)

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def get_next_secret(secret):
    secret = prune(mix(secret*64, secret))
    secret = prune(mix(secret//32, secret))
    secret = prune(mix(secret*2048, secret))
    return secret

def do_part(part):
    count = len(lines)
    secret = np.empty((count, 2001), dtype=int)
    secret[:,0] = INITIAL
    for i in range(2000):
        secret[:,i+1] = get_next_secret(secret[:,i])

    if part == 1:
        return secret[:,-1].sum()
    else:
        ones_digit = secret % 10
        diff = ones_digit[:,1:] - ones_digit[:,:-1]
        diff += 9
        width = diff.shape[1]

        base = 9*2 + 1
        num_combos = base**4
        combos = np.zeros(num_combos, dtype=int)
        coef = base ** np.arange(4)

        first = np.full((count, num_combos), True)
        row_indices = np.arange(count)

        for i in range(width - 3):
            index = diff[:,i:i+4] * coef
            index = index.sum(axis=-1)
            np.add.at(combos, index, ones_digit[:,i+4]*first[row_indices, index])
            first[row_indices, index] = False

        return np.max(combos)

def main():
    for part in [1, 2]:
        before = time.perf_counter()
        answer = do_part(part)
        after = time.perf_counter()
        elapsed = round((after - before)*1_000_000)
        unit = "µs"
        if elapsed >= 1000:
            elapsed //= 1000
            unit = "ms"
        print(f"Part {part}: {answer} ({elapsed:,} {unit})")

main()
