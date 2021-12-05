import dataclasses
from functools import cached_property
from typing import Union, Optional


@dataclasses.dataclass
class Coords2D:
    x: int
    y: int

    @classmethod
    def from_input_line(cls, input_line: str, sep: str = ",") -> "Coords2D":
        split = input_line.split(sep, 1)
        return cls(
            int(split[0]),
            int(split[1])
        )

    def __eq__(self, other: "Coords2D") -> bool:
        return isinstance(other, Coords2D) and self.x == other.x and self.y == other.y


@dataclasses.dataclass
class Line2D:
    start: Coords2D
    end: Coords2D

    @cached_property
    def min_x(self) -> int:
        return min(self.start.x, self.end.x)

    @cached_property
    def min_y(self) -> int:
        return min(self.start.y, self.end.y)

    @cached_property
    def max_x(self) -> int:
        return max(self.start.x, self.end.x)

    @cached_property
    def max_y(self) -> int:
        return max(self.start.y, self.end.y)

    @cached_property
    def len_x(self) -> int:
        return self.max_x - self.min_x

    @cached_property
    def len_y(self) -> int:
        return self.max_y - self.min_y

    @cached_property
    def vertical(self) -> bool:
        return self.start.x == self.end.x

    @cached_property
    def horizontal(self) -> bool:
        return self.start.y == self.end.y

    @cached_property
    def diagonal(self) -> bool:
        return self.len_x == self.len_y

    @cached_property
    def leading_diagonal(self) -> bool:
        if not self.diagonal:
            raise ValueError
        return self.start in [Coords2D(self.min_x, self.min_y), Coords2D(self.max_x, self.max_y)]

    @classmethod
    def from_input_line(cls, input_line: str) -> "Line2D":
        start, end = input_line.split(" -> ", 1)
        return cls(
            Coords2D.from_input_line(start),
            Coords2D.from_input_line(end)
        )


class Map2D:
    def __init__(self, width: int, height: int, fill: Optional[Union[str, int]] = None) -> None:
        self.map = []
        for _ in range(height):
            self.map.append([fill for _ in range(width)])
