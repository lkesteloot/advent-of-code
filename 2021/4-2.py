
import sys

def transpose(rows):
    return [[rows[j][i] for j in range(5)] for i in range(5)]

class Board:
    def __init__(self, lines):
        self.rows = [list(map(int, line.strip().split())) for line in lines]
        self.won = False

    def erase(self, number):
        self.rows = [[-1 if cell == number else cell for cell in row] for row in self.rows]

    def winner(self):
        return any(sum(row) == -5 for row in self.rows) or \
            any(sum(row) == -5 for row in transpose(self.rows))

    def score(self):
        return sum(sum(cell for cell in row if cell != -1) for row in self.rows)

lines = list(open("input-4-test.txt"))

numbers = map(int, lines[0].split(","))

boards = []
for i in range(2, len(lines), 6):
    boards.append(Board(lines[i:i+5]))

for number in numbers:
    for board in boards:
        board.erase(number)
        if board.winner() and not board.won:
            board.won = True
            if sum([0 if board.won else 1 for board in boards]) == 0:
                print(board.score()*number)
                #for board in boards:
                    #print(board.rows)
                sys.exit(0)

