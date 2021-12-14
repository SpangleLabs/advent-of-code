from collections import Counter, defaultdict
from typing import Dict, List
import typing

from utils.input import load_lines


def extend_polymer(polymer: typing.Counter[str], extensions: Dict[str, str]) -> typing.Counter[str]:
    new_counter = Counter()
    for key, val in polymer.items():
        first_key = key[0] + extensions[key]
        second_key = extensions[key] + key[1]
        new_counter[first_key] += val
        new_counter[second_key] += val
    return new_counter


if __name__ == "__main__":
    my_input = load_lines()
    input_polymer = [my_input[0][i:i+2] for i in range(len(my_input[0])-1)]
    ext_map = {
        l.split(" -> ")[0]: l.split(" -> ")[1] for l in my_input[2:]
    }
    input_counter = Counter(input_polymer)
    for step in range(40):
        print(step)
        input_counter = extend_polymer(input_counter, ext_map)
    char_counter = Counter()
    for k, v in input_counter.items():
        # char_counter[k[0]] += v
        char_counter[k[1]] += v
    # First char will be the same
    char_counter[input_polymer[0][0]] += 1
    most_common = char_counter.most_common()
    print(most_common[0][1] - most_common[-1][1])
