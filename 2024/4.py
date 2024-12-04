
import numpy as np
import scipy.signal as sig

BASE = 256

lines = open("input-4-test.txt").read().splitlines()
lines = open("input-4.txt").read().splitlines()

puzzle = np.array([[ord(ch) for ch in line] for line in lines])

# Make a list of all four 90 degree rotations of the matrix.
def four_rots(m):
    return [np.rot90(m, k=k) for k in range(4)]

def do_part(part):
    if part == 1:
        size = 4
        kernel = BASE ** np.arange(size)
        target_value = np.sum(np.array([ord(ch) for ch in "XMAS"]) * kernel)

        across = np.zeros((size, size), dtype=int)
        across[0] = kernel

        diagonal = np.zeros((size, size), dtype=int)
        np.fill_diagonal(diagonal, kernel)

        ms = four_rots(across) + four_rots(diagonal)
    else:
        kernel = np.array([
            [BASE**0,       0, BASE**1],
            [      0, BASE**2,       0],
            [BASE**3,       0, BASE**4],
        ])

        target_value = np.sum(np.array([
            [ord("M"),        0, ord("M")],
            [       0, ord("A"),        0],
            [ord("S"),        0, ord("S")],
        ]) * kernel)

        ms = four_rots(kernel)

    total = sum(np.count_nonzero(sig.convolve2d(puzzle, m) == target_value)
                for m in ms)

    print(f"Part {part}: {total}")

do_part(1)
do_part(2)
