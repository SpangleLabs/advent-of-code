from typing import Tuple, Callable

from utils.input import load_lines


class Lights:

    def __init__(self):
        self.grid = []
        for row in range(1000):
            self.grid.append([0] * 1000)

    def execute_cmd(self, start: Tuple[int, int], end: Tuple[int, int], cmd: Callable[[int], int]):
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                self.grid[x][y] = cmd(self.grid[x][y])

    def parse_line(self, line: str) -> None:
        line = line.replace("turn o", "turno")
        cmd, rest = line.split(" ", maxsplit=1)
        start, end = rest.split(" through ")
        start = tuple(int(x) for x in start.split(","))
        end = tuple(int(x) for x in end.split(","))
        cmd = {
            "turnon": lambda x: x+1,
            "turnoff": lambda x: max(0, x-1),
            "toggle": lambda x: x+2
        }[cmd]
        self.execute_cmd(start, end, cmd)

    def sum(self) -> int:
        return sum(sum(row) for row in self.grid)


if __name__ == "__main__":
    lights = Lights()
    for line in load_lines():
        lights.parse_line(line)
    print(lights.sum())
