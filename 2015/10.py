from typing import Tuple

from utils.input import load_input


def get_next_number(inp: str) -> Tuple[str, int]:
    first_number = inp[0]
    count = 0
    while inp.startswith(first_number):
        count += 1
        inp = inp[1:]
    return first_number, count


def construct_look_and_say(inp: str) -> str:
    out = ""
    while inp:
        char, count = get_next_number(inp)
        inp = inp[count:]
        out += f"{count}{char}"
    return out


if __name__ == "__main__":
    my_input = load_input()
    for step in range(40):
        my_input = construct_look_and_say(my_input)
    print(len(my_input))
