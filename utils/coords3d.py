import dataclasses
from typing import List

from utils.coords2d import Coords2D


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
