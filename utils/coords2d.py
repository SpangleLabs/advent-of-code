import dataclasses
from functools import cached_property
from typing import Union, Iterable, TypeVar, Generic, List, Optional


@dataclasses.dataclass(order=True, eq=True, frozen=True)
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

    def copy(self, *, x: int = None, y: int = None) -> "Coords2D":
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        return Coords2D(x, y)

    def __sub__(self, other: "Coords2D") -> "Coords2D":
        return Coords2D(
            self.x - other.x,
            self.y - other.y
        )

    def __add__(self, other: "Coords2D") -> "Coords2D":
        return Coords2D(
            self.x + other.x,
            self.y + other.y
        )

    def __hash__(self):
        return hash((self.x, self.y))

    def list_neighbours(self, with_diagonals: bool = False) -> List["Coords2D"]:
        neighbours = [
            Coords2D(self.x - 1, self.y),
            Coords2D(self.x, self.y - 1),
            Coords2D(self.x + 1, self.y),
            Coords2D(self.x, self.y + 1)
        ]
        if not with_diagonals:
            return neighbours
        neighbours.extend([
            Coords2D(self.x - 1, self.y - 1),
            Coords2D(self.x - 1, self.y + 1),
            Coords2D(self.x + 1, self.y - 1),
            Coords2D(self.x + 1, self.y + 1)
        ])
        return neighbours


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


T = TypeVar("T", bound=Union[None, str, int, bool, float])


class Map2D(Generic[T]):
    def __init__(self, width: int, height: int, fill: T = None) -> None:
        self.map = []
        for _ in range(height):
            self.map.append([fill for _ in range(width)])

    @property
    def width(self) -> int:
        return len(self.map[0])

    @property
    def height(self) -> int:
        return len(self.map)

    @property
    def size(self) -> int:
        return self.width * self.height

    def get_value(self, coords: Coords2D) -> T:
        return self.map[coords.y][coords.x]

    def try_get_value(self, coords: Coords2D, default: Optional[T] = None) -> Optional[T]:
        if self.valid_coords(coords):
            return self.get_value(coords)
        return default

    def set_value(self, coords: Coords2D, val: T) -> None:
        self.map[coords.y][coords.x] = val

    def set_value_if_smaller(self, coords: Coords2D, val: T) -> None:
        if self.map[coords.y][coords.x] > val:
            self.set_value(coords, val)

    def all_coords(self) -> Iterable[Coords2D]:
        for y, row in enumerate(self.map):
            for x in range(len(row)):
                yield Coords2D(x, y)

    @classmethod
    def from_number_input(cls, input_list: List[str]) -> "Map2D[int]":
        grid = cls(0, 0, fill=0)
        for line in input_list:
            grid.map.append([int(x) for x in line])
        return grid

    @classmethod
    def from_bool_input(cls, input_list: List[str], true_value: str = "1"):
        grid = cls(0, 0, fill=False)
        for line in input_list:
            grid.map.append([(x == true_value) for x in line])
        return grid

    def valid_coords(self, coords: Coords2D) -> bool:
        return (
            0 <= coords.x < self.width
            and 0 <= coords.y < self.height
        )

    def valid_neighbours(self, coords: Coords2D, with_diagonals: bool = False) -> List[Coords2D]:
        return [
            coord for coord in coords.list_neighbours(with_diagonals) if self.valid_coords(coord)
        ]

    def count(self, value: T) -> int:
        return sum(
            line.count(value)
            for line in self.map
        )
