from collections import Counter
from typing import Tuple, List

from utils.input import load_lines


def calculate_values(lines: List[str]) -> Tuple[int, int]:
    bit_length = len(lines[0])
    columns = [""] * bit_length
    for line in lines:
        for n, char in enumerate(line):
            columns[n] += char
    counters = [Counter(col) for col in columns]
    gamma_array = [max(counter, key=counter.get) for counter in counters]
    gamma = int("".join(gamma_array), base=2)
    epsilon_array = [str(1 - int(x)) for x in gamma_array]
    epsilon = int("".join(epsilon_array), base=2)
    return gamma, epsilon


if __name__ == "__main__":
    g, e = calculate_values(load_lines())
    print(g * e)
