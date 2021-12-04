from typing import List

from utils import load_lines


class BingoBoard:
    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid

    @classmethod
    def from_lines(cls, lines: List[str]) -> "BingoBoard":
        grid = [
            [int(num) for num in line.split()]
            for line in lines
        ]
        return BingoBoard(grid)

    def mark_number(self, called_num: int) -> None:
        for y, row in enumerate(self.grid):
            for x, num in enumerate(row):
                if num == called_num:
                    self.grid[y][x] = None

    def has_won(self) -> bool:
        for row in self.grid:
            if all(x is None for x in row):
                return True
        for col in range(len(self.grid[0])):
            if all(row[col] is None for row in self.grid):
                return True
        return False

    def sum(self) -> int:
        return sum(
            num for row in self.grid for num in row if num is not None
        )


def last_board_score(numbers: List[int], boards: List[BingoBoard]) -> int:
    for num in numbers:
        for card in boards:
            card.mark_number(num)
            if all(board.has_won() for board in boards):
                return card.sum() * num


def construct_boards(lines: List[str]) -> List[BingoBoard]:
    bingo_lines = []
    bingo_boards = []
    for line in lines:
        if not line.strip() and bingo_lines:
            bingo_boards.append(BingoBoard.from_lines(bingo_lines))
            bingo_lines = []
        else:
            bingo_lines.append(line)
    if bingo_lines:
        bingo_boards.append(BingoBoard.from_lines(bingo_lines))
    return bingo_boards


if __name__ == "__main__":
    my_input = load_lines()
    called_numbers = [int(called_number) for called_number in my_input[0].split(",")]
    # Construct boards
    bingo_boards = construct_boards(my_input[2:])
    # Call numbers
    print(last_board_score(called_numbers, bingo_boards))

