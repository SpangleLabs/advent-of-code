from typing import Optional

from utils.input import load_lines


def find_closing_chars(input_line: str) -> Optional[str]:
    stack = []
    brackets = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<"
    }
    brackets_inv = {v: k for k, v in brackets.items()}
    for char in input_line:
        if char not in brackets:
            stack.append(char)
        else:
            if stack[-1] == brackets[char]:
                stack = stack[:-1]
            else:
                return None
    return "".join(brackets_inv[char] for char in stack[::-1])


def points_for_line(input_line: str) -> Optional[int]:
    brackets = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }
    score = 0
    closing_chars = find_closing_chars(input_line)
    if closing_chars is None:
        return None
    for char in closing_chars:
        score *= 5
        score += brackets[char]
    return score


if __name__ == "__main__":
    scores = []
    for line in load_lines():
        line_score = points_for_line(line)
        if line_score is not None:
            scores.append(points_for_line(line))
    scores = sorted(scores)
    print(scores[len(scores) // 2])
