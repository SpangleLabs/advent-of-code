from collections import Counter

from utils.input import load_input


if __name__ == "__main__":
    visits = Counter()
    coords = (0, 0)
    cmds = {
        "v": lambda c: (c[0], c[1] - 1),
        ">": lambda c: (c[0] + 1, c[1]),
        "^": lambda c: (c[0], c[1] + 1),
        "<": lambda c: (c[0] - 1, c[1])
    }
    visits[coords] += 1
    for cmd in load_input().strip():
        coords = cmds[cmd](coords)
        visits[coords] += 1
    print(len(visits))
