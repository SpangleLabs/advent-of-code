import re

from utils.input import load_lines


def in_memory_size(line: str) -> int:
    char_pattern = re.compile(r"\\\\|\\\"|\\x[0-9a-f]{2}")
    line = line[1:-1]
    line = char_pattern.sub("a", line)
    return len(line)


def embiggen(line: str) -> str:
    char_pattern = re.compile(r"([\\\"])")
    line = char_pattern.sub("\\\1", line)
    return f"\"{line}\""


if __name__ == "__main__":
    total_diff = 0
    for l in load_lines():
        total_diff += len(embiggen(l)) - len(l)
    print(total_diff)
