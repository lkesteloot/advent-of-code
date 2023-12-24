
import re
from itertools import combinations
import numpy as np

part2 = True

if False:
    lines = open("input-24-test.txt").read().splitlines()
    minc = 7
    maxc = 27
else:
    lines = open("input-24.txt").read().splitlines()
    minc = 200000000000000
    maxc = 400000000000000

hails = [tuple(map(int, re.findall(r'[-0-9]+', line))) for line in lines]

if part2:
    def fun(xyz):
        t1, t2, t3, ox, oy, oz, dx, dy, dz = xyz
        rows = []
        hox, hoy, hoz, hdx, hdy, hdz = hails[0]
        rows.extend([
            hdx*t1 - dx*t1 + hox - ox,
            hdy*t1 - dy*t1 + hoy - oy,
            hdz*t1 - dz*t1 + hoz - oz,
        ])
        hox, hoy, hoz, hdx, hdy, hdz = hails[1]
        rows.extend([
            hdx*t2 - dx*t2 + hox - ox,
            hdy*t2 - dy*t2 + hoy - oy,
            hdz*t2 - dz*t2 + hoz - oz,
        ])
        hox, hoy, hoz, hdx, hdy, hdz = hails[4]
        rows.extend([
            hdx*t3 - dx*t3 + hox - ox,
            hdy*t3 - dy*t3 + hoy - oy,
            hdz*t3 - dz*t3 + hoz - oz,
        ])
        return rows

    def jacobian(xyz):
        t1, t2, t3, ox, oy, oz, dx, dy, dz = xyz
        rows = []
        hox, hoy, hoz, hdx, hdy, hdz = hails[0]
        rows.extend([
            [ hdx - dx, 0, 0, -1, 0, 0, -t1, 0, 0, ],
            [ hdy - dy, 0, 0, 0, -1, 0, 0, -t1, 0, ],
            [ hdz - dz, 0, 0, 0, 0, -1, 0, 0, -t1, ],
        ])
        hox, hoy, hoz, hdx, hdy, hdz = hails[1]
        rows.extend([
            [ 0, hdx - dx, 0, -1, 0, 0, -t2, 0, 0, ],
            [ 0, hdy - dy, 0, 0, -1, 0, 0, -t2, 0, ],
            [ 0, hdz - dz, 0, 0, 0, -1, 0, 0, -t2, ],
        ])
        hox, hoy, hoz, hdx, hdy, hdz = hails[4]
        rows.extend([
            [ 0, 0, hdx - dx, -1, 0, 0, -t3, 0, 0, ],
            [ 0, 0, hdy - dy, 0, -1, 0, 0, -t3, 0, ],
            [ 0, 0, hdz - dz, 0, 0, -1, 0, 0, -t3, ],
        ])
        return rows

    rng = np.random.default_rng()
    x = rng.random(9)

    answers = set()
    for k in range(50):
        J = np.array(jacobian(x))
        F = np.array(fun(x))

        diff = np.linalg.solve(J, -F)
        x += diff

        answer = int(sum(x[3:6]))
        answers.add(answer)

        if np.linalg.norm(diff) < 1e-8:
            break
    else:
        print("did not converge")

    print("pick one of these", list(sorted(x for x in answers if abs(x - answer) < 5)))
else:
    def intersects(a, b, minc, maxc):
        a0 = np.array(a[0:2])
        ad = np.array(a[3:5])
        b0 = np.array(b[0:2])
        bd = np.array(b[3:5])

        m = np.column_stack([ad, -bd])
        y = np.array(b0 - a0)

        try:
            ta, tb = np.linalg.solve(m, y)
        except np.linalg.LinAlgError:
            return False

        pt = ad*ta + a0

        return ta >= 0 and tb >= 0 and \
                minc <= pt[0] <= maxc and \
                minc <= pt[1] <= maxc

    print(sum(intersects(a, b, minc, maxc) for a, b, in combinations(hails, 2)))

