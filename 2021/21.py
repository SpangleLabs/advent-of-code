import datetime
import string
from typing import Dict, List

from utils.input import load_lines
from utils.math import wrap


class Dice:
    def __init__(self):
        self.last_roll = 0
        self.roll_count = 0

    def roll(self) -> int:
        self.roll_count += 1
        self.last_roll += 1
        if self.last_roll > 100:
            self.last_roll = 1
        return self.last_roll


class Board:
    def __init__(self, dice: Dice, player_locations: Dict[int, int]):
        self.places = 10
        self.dice = dice
        self.player_locations = player_locations
        self.player_scores = {player: 0 for player in player_locations.keys()}

    def player_turn(self, player: int) -> None:
        move_forward = sum(self.dice.roll() for _ in range(3))
        new_position = wrap(self.player_locations[player] + move_forward, self.places)
        self.player_scores[player] += new_position
        self.player_locations[player] = new_position

    def game_won(self) -> bool:
        return max(score for score in self.player_scores.values()) >= 1000

    @classmethod
    def parse_input(cls, input_lines: List[str]) -> "Board":
        player_locations = {}
        for line in input_lines:
            first, second = line.split(": ")
            player_num = int(first.strip(string.ascii_letters + string.whitespace))
            player_loc = int(second)
            player_locations[player_num] = player_loc
        return cls(Dice(), player_locations)


def _main() -> str:
    my_input = load_lines()
    board = Board.parse_input(my_input)
    while not board.game_won():
        for player in board.player_locations.keys():
            board.player_turn(player)
            if board.game_won():
                break
    result = board.dice.roll_count * min(board.player_scores.values())
    return str(result)


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
