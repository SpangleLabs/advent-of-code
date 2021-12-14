from collections import Counter
from typing import Dict, List

from utils.input import load_lines


def extend_polymer(polymer: List[str], extensions: Dict[str, str]) -> List[str]:
    for index in range(len(polymer) - 1, 0, -1):
        key = polymer[index - 1] + polymer[index]
        polymer.insert(index, extensions[key])
    return polymer


if __name__ == "__main__":
    my_input = load_lines()
    input_polymer = list(my_input[0])
    ext_map = {
        l.split(" -> ")[0]: l.split(" -> ")[1] for l in my_input[2:]
    }
    for step in range(10):
        extend_polymer(input_polymer, ext_map)
    c = Counter(input_polymer)
    most_common = c.most_common()
    print(most_common[0][1] - most_common[-1][1])
