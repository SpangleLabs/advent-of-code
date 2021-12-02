from utils import load_lines


def is_nice(line: str) -> bool:
    vowel_count = sum(line.count(vowel) for vowel in "aeiou")
    if vowel_count < 3:
        return False
    if any(sub in line for sub in ["ab", "cd", "pq", "xy"]):
        return False
    if any(l*2 in line for l in "abcdefghijklmnopqrstuvwxyz"):
        return True
    return False


if __name__ == "__main__":
    nice_count = 0
    for line in load_lines():
        if is_nice(line):
            nice_count += 1
    print(nice_count)
