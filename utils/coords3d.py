import dataclasses
from typing import List, Optional, Iterable

from utils.coords2d import Coords2D, Map2D, T


@dataclasses.dataclass(order=True, eq=True, frozen=True)
class Coords3D(Coords2D):
    x: int
    y: int
    z: int

    @classmethod
    def from_input_line(cls, input_line: str, sep: str = ",") -> "Coords3D":
        split = input_line.split(sep, 2)
        return cls(
            int(split[0]),
            int(split[1]),
            int(split[2])
        )

    def copy(self, *, x: int = None, y: int = None, z: int = None) -> "Coords3D":
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if z is None:
            z = self.z
        return Coords3D(x, y, z)

    def __sub__(self, other: "Coords3D") -> "Coords3D":
        return Coords3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __add__(self, other: "Coords3D") -> "Coords3D":
        return Coords3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __neg__(self) -> "Coords3D":
        return Coords3D(
            -self.x,
            -self.y,
            -self.z
        )

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def list_neighbours(self, with_diagonals: bool = False) -> List["Coords3D"]:
        raise NotImplementedError


class Map3D(Map2D):

    def __init__(self, width: int, height: int, depth: int, fill: T = None) -> None:
        super().__init__(width, height)
        self.map = []
        for _ in range(height):
            layer = []
            for __ in range(width):
                layer.append([fill for _ in range(depth)])
            self.map.append(layer)

    @property
    def height(self) -> int:
        return len(self.map)

    @property
    def width(self) -> int:
        if self.height == 0:
            return 0
        return len(self.map[0])

    @property
    def depth(self) -> int:
        if self.height == 0 or self.width == 0:
            return 0
        return len(self.map[0][0])

    @property
    def size(self) -> int:
        return self.width * self.height * self.depth

    def get_value(self, coords: Coords3D) -> T:
        return self.map[coords.y][coords.x][coords.z]

    def try_get_value(self, coords: Coords3D, default: Optional[T] = None) -> Optional[T]:
        if self.valid_coords(coords):
            return self.get_value(coords)
        return default

    def set_value(self, coords: Coords3D, val: T) -> None:
        self.map[coords.y][coords.x][coords.z] = val

    def set_value_if_smaller(self, coords: Coords3D, val: T) -> None:
        if self.map[coords.y][coords.x][coords.z] > val:
            self.set_value(coords, val)

    def all_coords(self) -> Iterable[Coords3D]:
        for y, layer in enumerate(self.map):
            for x, row in enumerate(layer):
                for z in range(len(row)):
                    yield Coords3D(x, y, z)

    def all_coords_with_value(self, value: T) -> Iterable[Coords3D]:
        for y, layer in enumerate(self.map):
            for x, row in enumerate(layer):
                for z, val in enumerate(row):
                    if val == value:
                        yield Coords3D(x, y, z)

    @classmethod
    def from_number_input(cls, input_list: List[str]) -> "Map3D[int]":
        raise NotImplementedError

    @classmethod
    def from_bool_input(cls, input_list: List[str], true_value: str = "1"):
        raise NotImplementedError

    def valid_coords(self, coords: Coords3D) -> bool:
        return (
            0 <= coords.x < self.width
            and 0 <= coords.y < self.height
            and 0 <= coords.z < self.depth
        )

    def valid_neighbours(self, coords: Coords3D, with_diagonals: bool = False) -> List[Coords3D]:
        return [
            coord for coord in coords.list_neighbours(with_diagonals) if self.valid_coords(coord)
        ]

    def count(self, value: T) -> int:
        return sum(
            line.count(value)
            for layer in self.map
            for line in layer
        )
