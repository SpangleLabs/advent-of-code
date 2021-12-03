from collections import Counter
from typing import List, Callable

from utils import load_lines


def filter_matching(lines: List[str], bit_criteria: Callable[[str, str], bool]) -> int:
    maybe_matching = lines[:]
    for n in range(len(lines[0])):
        char_counter = Counter(line[n] for line in maybe_matching)
        max_char = "1" if char_counter["1"] >= char_counter["0"] else "0"
        for line in maybe_matching[:]:
            if len(maybe_matching) == 1:
                return int(maybe_matching[0], base=2)
            if not bit_criteria(line[n], max_char):
                maybe_matching.remove(line)
        if len(maybe_matching) == 1:
            return int(maybe_matching[0], base=2)


def calculate_oxygen(lines: List[str]) -> int:
    criteria = lambda char, max_char: char == max_char
    return filter_matching(lines, criteria)


def calculate_carbon(lines: List[str]) -> int:
    criteria = lambda char, max_char: char != max_char
    return filter_matching(lines, criteria)


if __name__ == "__main__":
    my_input = load_lines()
    oxygen = calculate_oxygen(my_input)
    carbon = calculate_carbon(my_input)
    print(oxygen * carbon)
