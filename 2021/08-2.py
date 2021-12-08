import dataclasses
from typing import List, Set

from utils.input import load_lines


@dataclasses.dataclass
class DisplayNumber:
    top_bar: bool
    mid_bar: bool
    bot_bar: bool
    left_top: bool
    left_bot: bool
    right_top: bool
    right_bot: bool

    def to_binary(self) -> str:
        return "".join([
            "1" if self.top_bar else "0",
            "1" if self.mid_bar else "0",
            "1" if self.bot_bar else "0",
            "1" if self.left_top else "0",
            "1" if self.left_bot else "0",
            "1" if self.right_top else "0",
            "1" if self.right_bot else "0"
        ])

    def value(self) -> int:
        return {
            "1011111": 0,
            "0000011": 1,
            "1110110": 2,
            "1110011": 3,
            "0101011": 4,
            "1111001": 5,
            "1111101": 6,
            "1000011": 7,
            "1111111": 8,
            "1111011": 9
        }[self.to_binary()]



@dataclasses.dataclass
class DisplayWiring:
    top_bar: str
    mid_bar: str
    bot_bar: str
    left_top: str
    left_bot: str
    right_top: str
    right_bot: str

    def set_segments(self, segments: List[str]) -> DisplayNumber:
        return DisplayNumber(
            self.top_bar in segments,
            self.mid_bar in segments,
            self.bot_bar in segments,
            self.left_top in segments,
            self.left_bot in segments,
            self.right_top in segments,
            self.right_bot in segments
        )


def single_set_element(input_set: Set[str]) -> str:
    if len(input_set) != 1:
        raise ValueError("Set has more than 1 element")
    return list(input_set)[0]


def find_wiring(input_digits: List[str]) -> DisplayWiring:
    # Make sets of display parts for each known number
    one = None
    four = None
    seven = None
    eight = None
    # And lists of sets for uncertain numbers
    five_segments = []  # Numbers: 2, 3, 5
    six_segments = []  # Three numbers: 0, 6, 9

    # Drop inputs into buckets
    for input_digit in input_digits:
        if len(input_digit) == 2:
            one = set(input_digit)
        elif len(input_digit) == 3:
            seven = set(input_digit)
        elif len(input_digit) == 4:
            four = set(input_digit)
        elif len(input_digit) == 7:
            eight = set(input_digit)
        elif len(input_digit) == 5:
            five_segments.append(set(input_digit))
        elif len(input_digit) == 6:
            six_segments.append(set(input_digit))
        else:
            raise ValueError("Unrecognised input digit")

    if len(five_segments) != len(six_segments) != 3:
        raise ValueError("Didn't find all five and six segment input digits")

    if one is None or seven is None or four is None or eight is None:
        raise ValueError("Didn't find all distinct digits")

    # We know the top bar, thanks to 1 and 7
    top_bar = single_set_element(seven - one)

    # Find 6 by intersection with 1
    six = None
    for input_set in six_segments[:]:
        if len(input_set.intersection(one)) == 1:
            six = input_set
            six_segments.remove(input_set)
            break
    if six is None:
        raise ValueError("Could not find six")

    # Set the right bars
    right_bot = single_set_element(six.intersection(one))
    right_top = single_set_element(one - {right_bot})

    # Find nine and zero by difference with 4
    zero = None
    nine = None
    for input_set in six_segments:
        if len(input_set - four) == 2:
            nine = input_set
        else:
            zero = input_set
    if nine is None or zero is None:
        raise ValueError("Could not find nine and zero")

    # Set mid bar and left bot
    mid_bar = single_set_element(eight - zero)
    left_bot = single_set_element(eight - nine)

    # Set left top from 4
    left_top = single_set_element(four - {right_top, right_bot, mid_bar})

    # Set bottom bar from leftover
    bot_bar = single_set_element(eight - {top_bar, mid_bar, left_top, left_bot, right_top, right_bot})

    return DisplayWiring(
        top_bar, mid_bar, bot_bar, left_top, left_bot, right_top, right_bot
    )


if __name__ == "__main__":
    total = 0
    for line in load_lines():
        inp, results = line.split(" | ")
        wiring = find_wiring(inp.split())
        result_digits = []
        for result in results.split():
            result_digit = wiring.set_segments(list(result))
            result_digits.append(result_digit.value())
        total += int("".join(str(d) for d in result_digits))
    print(total)
