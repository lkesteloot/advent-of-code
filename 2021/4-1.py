
import sys

class Board:
    def __init__(self, lines):
        self.rows = [list(map(int, line.strip().split())) for line in lines]

    def erase(self, number):
        self.rows = [[-1 if cell == number else cell for cell in row] for row in self.rows]

    def winner(self):
        column = [0]*5
        for row in self.rows:
            if sum(row) == -5:
                return True

            for i in range(5):
                column[i] += row[i]

        for column in column:
            if column == -5:
                return True

        return False

    def score(self):
        return sum(sum(cell for cell in row if cell != -1) for row in self.rows)

lines = list(open("input-4.txt"))

numbers = map(int, lines[0].split(","))

boards = []
for i in range(2, len(lines), 6):
    boards.append(Board(lines[i:i+5]))

for number in numbers:
    for board in boards:
        board.erase(number)
        if board.winner():
            print(board.score()*number)
            #for board in boards:
                #print(board.rows)
            sys.exit(0)

