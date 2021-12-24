import datetime
import string
from typing import Dict, List

from utils.input import load_lines
from utils.math import wrap


class Board:
    def __init__(self, player_locations: Dict[int, int]):
        self.places = 10
        self.dice_sides = 3
        self.states = [BoardState(player_locations[1], player_locations[2], 0, 0)]
        self.games_won = {player: 0 for player in player_locations.keys()}

    def player_turn(self, player: int) -> None:
        new_locations = {
            3: 1,
            4: 3,
            5: 6,
            6: 7,
            7: 6,
            8: 3,
            9: 1
        }
        new_states = []
        for move, count in new_locations.items():
            for state in self.states:
                new_state = state.with_player_turn(player, move, count)
                if new_state.game_won():
                    self.games_won[new_state.winning_player()] += new_state.count
                else:
                    new_states.append(new_state)
        self.states = new_states

    def games_over(self) -> bool:
        return not self.states

    @classmethod
    def parse_input(cls, input_lines: List[str]) -> "Board":
        player_locations = {}
        for line in input_lines:
            first, second = line.split(": ")
            player_num = int(first.strip(string.ascii_letters + string.whitespace))
            player_loc = int(second)
            player_locations[player_num] = player_loc
        return cls(player_locations)


class BoardState:
    def __init__(self, p1_loc: int, p2_loc: int, p1_score: int, p2_score: int, count: int = 1):
        self.p1_loc = p1_loc
        self.p2_loc = p2_loc
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.count = count

    def game_won(self) -> bool:
        return max([self.p1_score, self.p2_score]) >= 21

    def winning_player(self) -> int:
        return 1 if self.p1_score > self.p2_score else 2

    def with_player_turn(self, player: int, move: int, count: int) -> "BoardState":
        if player == 1:
            new_position = wrap(self.p1_loc + move, 10)
            new_score = self.p1_score + new_position
            return BoardState(
                new_position,
                self.p2_loc,
                new_score,
                self.p2_score,
                self.count * count
            )
        else:
            new_position = wrap(self.p2_loc + move, 10)
            new_score = self.p2_score + new_position
            return BoardState(
                self.p1_loc,
                new_position,
                self.p1_score,
                new_score,
                self.count * count
            )


def _main() -> str:
    my_input = load_lines()
    board = Board.parse_input(my_input)
    while not board.games_over():
        for player in board.games_won.keys():
            board.player_turn(player)
            print(len(board.states))
            if board.games_over():
                break
    result = max(board.games_won.values())
    return str(result)


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
