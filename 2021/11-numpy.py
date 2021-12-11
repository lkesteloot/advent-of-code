
import numpy as np
import scipy.signal

neighbors = np.full((3, 3), 1)
neighbors[1, 1] = 0

o = np.array(list(map(int, open("input-11.txt").read().replace("\n", "")))).reshape(10, 10)

total_flashes = 0
for step in range(1, 10000):
    o += 1

    flashed = np.full(o.shape, False)
    while True:
        flashed_now = (o > 9) & np.logical_not(flashed)
        if not flashed_now.any():
            break

        flashed |= flashed_now
        o += scipy.signal.convolve2d(flashed_now, neighbors, mode="same")

    total_flashes += flashed.sum()
    o[flashed] = 0

    if flashed.all():
        print("all flashed", step)
        break

    if step == 100:
        print(total_flashes)





