
import time
from collections import defaultdict
from intcode import Intcode, parse_mem

data = open("input-11.txt").read()
MEM = parse_mem(data)

def add(p, d):
    return p[0] + d[0], p[1] + d[1]

class HullPaintingRobot(Intcode):
    def __init__(self, mem, tiles):
        super().__init__(mem)
        self.tiles = tiles
        self.position = 0,0
        self.direction = 0,-1 # up
        self.expecting_color = True

    def input(self):
        return self.tiles[self.position]

    def output(self, v):
        if self.expecting_color:
            self.tiles[self.position] = v
        else:
            if v == 0:
                self.direction = self.direction[1], -self.direction[0]
            else:
                self.direction = -self.direction[1], self.direction[0]
            self.position = add(self.position, self.direction)

        self.expecting_color = not self.expecting_color

def do_part(part):
    # Map from (x,y) to color (0 or 1).
    tiles = defaultdict(int)

    if part == 1:
        robot = HullPaintingRobot(MEM, tiles)
        robot.run()
        return len(tiles)
    else:
        tiles[0,0] = 1
        robot = HullPaintingRobot(MEM, tiles)
        robot.run()
        min_x = min(x for x,_ in tiles)
        min_y = min(y for _,y in tiles)
        max_x = max(x for x,_ in tiles)
        max_y = max(y for _,y in tiles)
        for y in range(min_y, max_y + 1):
            print("".join(".#"[tiles[x,y]] for x in range(min_x, max_x + 1)))

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
