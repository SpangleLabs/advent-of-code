import dataclasses

from utils.input import load_lines


@dataclasses.dataclass
class Coords:
    horizontal: int
    depth: int
    aim: int

    def forward(self, num) -> "Coords":
        self.horizontal += num
        self.depth += num * self.aim
        return self

    def up(self, num) -> "Coords":
        self.aim -= num
        return self

    def down(self, num) -> "Coords":
        self.aim += num
        return self

    def route_command(self, cmd, num) -> None:
        {
            "forward": self.forward,
            "up": self.up,
            "down": self.down
        }[cmd](num)


if __name__ == "__main__":
    coords = Coords(0, 0, 0)
    for line in load_lines():
        cmd, num_str = line.split()
        num = int(num_str)
        coords.route_command(cmd, num)
    print(coords.horizontal * coords.depth)
