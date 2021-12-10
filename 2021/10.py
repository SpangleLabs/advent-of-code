from typing import Optional

from utils.input import load_lines


def find_incorrect_char(input_line: str) -> Optional[str]:
    stack = []
    brackets = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<"
    }
    for char in input_line:
        if char not in brackets:
            stack.append(char)
        else:
            if stack[-1] == brackets[char]:
                stack = stack[:-1]
            else:
                return char


def points_for_line(input_line: str) -> int:
    brackets = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }
    return brackets.get(find_incorrect_char(input_line), 0)


if __name__ == "__main__":
    total = 0
    for line in load_lines():
        total += points_for_line(line)
    print(total)
