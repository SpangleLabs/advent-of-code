import re

from utils.input import load_lines


def in_memory_size(line: str) -> int:
    char_pattern = re.compile(r"\\\\|\\\"|\\x[0-9a-f]{2}")
    line = line[1:-1]
    line = char_pattern.sub("a", line)
    return len(line)


if __name__ == "__main__":
    total_diff = 0
    for l in load_lines():
        total_diff += len(l) - in_memory_size(l)
    print(total_diff)
