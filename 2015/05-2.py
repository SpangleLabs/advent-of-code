import re

from utils.input import load_lines


def is_nice(line: str) -> bool:
    if not re.search(r"([a-z][a-z])[a-z]*\1", line):
        return False
    if re.search(r"([a-z])[a-z]\1", line):
        return True
    return False


if __name__ == "__main__":
    nice_count = 0
    for line in load_lines():
        if is_nice(line):
            nice_count += 1
    print(nice_count)
