
import time
from intcode import Intcode, parse_mem

data = open("input-13.txt").read()
MEM = parse_mem(data)

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

class ArcadeCabinet(Intcode):
    def __init__(self, mem):
        super().__init__(mem)
        # Map from (x,y) to tile id.
        self.tiles = {}
        self.score = 0
        self.outputs = []

    def input(self):
        #self.print()
        ball_x, _ = self.position_of(BALL)
        paddle_x, _ = self.position_of(PADDLE)
        if ball_x < paddle_x:
            return -1
        elif ball_x > paddle_x:
            return 1
        else:
            return 0

    def output(self, v):
        self.outputs.append(v)
        if len(self.outputs) == 3:
            x, y, tile_id = self.outputs
            if x == -1 and y == 0:
                self.score = tile_id
            else:
                self.tiles[x,y] = tile_id
            self.outputs = []

    def position_of(self, desired_tile_id):
        positions = [(x,y)
                     for (x,y),tile_id in self.tiles.items()
                     if tile_id == desired_tile_id]
        assert len(positions) == 1
        return positions[0]

    def num_blocks(self):
        return sum(1 for tile_id in self.tiles.values() if tile_id == BLOCK)

    def print(self):
        print("-"*50, self.score)
        min_x = min(x for x,_ in self.tiles)
        min_y = min(y for _,y in self.tiles)
        max_x = max(x for x,_ in self.tiles)
        max_y = max(y for _,y in self.tiles)
        for y in range(min_y, max_y + 1):
            print("".join(" #.-O"[self.tiles[x,y]]
                          for x in range(min_x, max_x + 1)))

def do_part(part):
    if part == 1:
        arcade_cabinet = ArcadeCabinet(MEM)
        arcade_cabinet.run()
        return arcade_cabinet.num_blocks()
    else:
        arcade_cabinet = ArcadeCabinet([2] + MEM[1:])
        arcade_cabinet.run()
        return arcade_cabinet.score

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
