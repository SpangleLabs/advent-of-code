import dataclasses
from typing import List

from utils.input import load_lines
from utils.coords2d import Coords2D, Line2D, Map2D


class Map(Map2D):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height, 0)

    def render(self) -> str:
        return "\n".join(
            "".join(str(val) or "." for val in row)
            for row in self.map
        )

    def num_overlaps(self, min_overlap: int = 2) -> int:
        return sum(
            sum(1 if val >= min_overlap else 0 for val in row)
            for row in self.map
        )

    def add_line(self, line: "Line") -> None:
        if line.vertical:
            for y in range(line.min_y, line.max_y + 1):
                self.map[y][line.start.x] += 1
            return
        if line.horizontal:
            for x in range(line.min_x, line.max_x + 1):
                self.map[line.start.y][x] += 1
            return
        raise NotImplementedError


@dataclasses.dataclass
class Line(Line2D):

    def is_valid(self) -> bool:
        return self.horizontal or self.vertical


def find_map_dimensions(lines: List[Line]) -> Coords2D:
    max_x = 0
    max_y = 0
    for line in lines:
        max_x = max(max_x, line.max_x)
        max_y = max(max_y, line.max_y)
    return Coords2D(max_x + 1, max_y + 1)


if __name__ == "__main__":
    my_input = load_lines()
    vent_lines = [Line.from_input_line(l) for l in my_input]
    dimensions = find_map_dimensions(vent_lines)
    my_map = Map(dimensions.x, dimensions.y)
    for vent_line in vent_lines:
        if vent_line.is_valid():
            my_map.add_line(vent_line)
    print(my_map.render())
    print(my_map.num_overlaps())
