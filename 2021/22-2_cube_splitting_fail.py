import dataclasses
import datetime
from functools import lru_cache
from typing import Optional, List, Set, Union

from utils.coords3d import Coords3D
from utils.input import load_lines


@dataclasses.dataclass(order=True, eq=True, frozen=True)
class CornerCoords3D:
    x: float
    y: float
    z: float

    @classmethod
    def from_coords(cls, coords: Coords3D) -> "CornerCoords3D":
        return cls(
            coords.x,
            coords.y,
            coords.z
        )

    def __add__(self, other: "CornerCoords3D") -> "CornerCoords3D":
        return CornerCoords3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other: "CornerCoords3D") -> "CornerCoords3D":
        return CornerCoords3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )


class Cuboid:
    def __init__(self, start: Coords3D, end: Coords3D) -> None:
        self.start = start
        self.end = end

    def __eq__(self, other: "Cuboid") -> bool:
        return self.start == other.start and self.end == other.end

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __repr__(self) -> str:
        return f"Cuboid({self.start}, {self.end})"

    @property
    def size(self) -> int:
        return (
            (1 + self.end.x - self.start.x)
            * (1 + self.end.y - self.start.y)
            * (1 + self.end.z - self.start.z)
        )

    def corners(self) -> Set[CornerCoords3D]:
        s = CornerCoords3D.from_coords(self.start) - CornerCoords3D(0.5, 0.5, 0.5)
        e = CornerCoords3D.from_coords(self.end) + CornerCoords3D(0.5, 0.5, 0.5)
        return {
            CornerCoords3D(s.x, s.y, s.z),
            CornerCoords3D(s.x, s.y, e.z),
            CornerCoords3D(s.x, e.y, s.z),
            CornerCoords3D(s.x, e.y, e.z),
            CornerCoords3D(e.x, s.y, s.z),
            CornerCoords3D(e.x, s.y, e.z),
            CornerCoords3D(e.x, e.y, s.z),
            CornerCoords3D(e.x, e.y, e.z)
        }

    @lru_cache
    def contains(self, coord: Union[Coords3D, CornerCoords3D]) -> bool:
        return (
            (self.start.x <= coord.x <= self.end.x)
            and (self.start.y <= coord.y <= self.end.y)
            and (self.start.z <= coord.z <= self.end.z)
        )

    def split(self, coord: CornerCoords3D) -> List["Cuboid"]:
        if not self.contains(coord):
            return [self]
        st = self.start
        ms = Coords3D(int(coord.x), int(coord.y), int(coord.z))
        me = ms + Coords3D(1, 1, 1)
        en = self.end
        return [
            c for c in [
                Cuboid(Coords3D(st.x, st.y, st.z), Coords3D(ms.x, ms.y, ms.z)),
                Cuboid(Coords3D(st.x, st.y, me.z), Coords3D(ms.x, ms.y, en.z)),
                Cuboid(Coords3D(st.x, me.y, st.z), Coords3D(ms.x, en.y, ms.z)),
                Cuboid(Coords3D(st.x, me.y, me.z), Coords3D(ms.x, en.y, en.z)),
                Cuboid(Coords3D(me.x, st.y, st.z), Coords3D(en.x, ms.y, ms.z)),
                Cuboid(Coords3D(me.x, st.y, me.z), Coords3D(en.x, ms.y, en.z)),
                Cuboid(Coords3D(me.x, me.y, st.z), Coords3D(en.x, en.y, ms.z)),
                Cuboid(Coords3D(me.x, me.y, me.z), Coords3D(en.x, en.y, en.z))
            ]
            if c.size > 0
        ]

    def split_by_all_corners(self, corners: Set[CornerCoords3D]) -> Set["Cuboid"]:
        out_cuboids: Set[Cuboid] = {self}
        for corner in corners:
            for cuboid in out_cuboids.copy():
                if cuboid.contains(corner):
                    out_cuboids.discard(cuboid)
                    out_cuboids.update(cuboid.split(corner))
        return out_cuboids


class Intersection(Cuboid):

    def __init__(self, start: Coords3D, end: Coords3D, depth: int):
        super().__init__(start, end)
        self.depth = depth

    def intersection(self, other: "Intersection") -> Optional["Intersection"]:
        start = Coords3D(
            max([self.start.x, other.start.x]),
            max([self.start.y, other.start.y]),
            max([self.start.z, other.start.z])
        )
        end = Coords3D(
            min([self.end.x, other.end.x]),
            min([self.end.y, other.end.y]),
            min([self.end.z, other.end.z])
        )
        cuboid = Intersection(start, end, self.depth + other.depth)
        if cuboid.size > 0:
            return cuboid
        return None


def intersection(one: Cuboid, two: Cuboid) -> Set[Cuboid]:
    return one.split_by_all_corners(two.corners()) | two.split_by_all_corners(one.corners())


def all_corners(cuboids: Set[Cuboid]) -> Set[CornerCoords3D]:
    corners = set()
    for cuboid in cuboids:
        corners.update(cuboid.corners())
    return corners


def add_intersection(cuboids: Set[Cuboid], new_cuboid: Cuboid) -> Set[Cuboid]:
    cuboid_corners = all_corners(cuboids)
    split_mine = new_cuboid.split_by_all_corners(cuboid_corners)
    my_corners = all_corners(split_mine)
    out = split_mine
    for cuboid in cuboids:
        out.update(cuboid.split_by_all_corners(my_corners))
    return out


def remove_intersection(cuboids: Set[Cuboid], new_cuboid: Cuboid) -> Set[Cuboid]:
    cuboid_corners = all_corners(cuboids)
    split_mine = new_cuboid.split_by_all_corners(cuboid_corners)
    my_corners = all_corners(split_mine)
    out = set()
    for cuboid in cuboids:
        out.update(cuboid.split_by_all_corners(my_corners))
    out -= split_mine
    return out


class Instruction:

    def __init__(self, start: Coords3D, end: Coords3D, state: bool):
        self.cuboid = Cuboid(start, end)
        self.state = state

    @classmethod
    def parse_input(cls, line: str) -> "Instruction":
        state, coords = line.split()
        x_str, y_str, z_str = coords.split(",")
        x_vals = [int(x) for x in x_str.lstrip("x=").split("..")]
        y_vals = [int(y) for y in y_str.lstrip("y=").split("..")]
        z_vals = [int(z) for z in z_str.lstrip("z=").split("..")]
        return cls(
            Coords3D(min(x_vals), min(y_vals), min(z_vals)),
            Coords3D(max(x_vals), max(y_vals), max(z_vals)),
            state == "on"
        )

    def __repr__(self) -> str:
        return f"Instruction({self.cuboid}, {self.state})"


class Reactor:

    def __init__(self):
        self.cuboids = set()

    def apply_instruction(self, instruction: Instruction) -> None:
        if instruction.state:
            self.cuboids = add_intersection(self.cuboids, instruction.cuboid)
        else:
            self.cuboids = remove_intersection(self.cuboids, instruction.cuboid)
        print(len(self.cuboids))

    def count_on(self) -> int:
        return sum(
            cuboid.size for cuboid in self.cuboids
        )


def _test() -> None:
    cube1 = Cuboid(Coords3D(0, 0, 0), Coords3D(10, 10, 0))
    cube2 = Cuboid(Coords3D(5, 5, 0), Coords3D(15, 15, 0))
    assert cube1.size == 121
    assert cube2.size == 121
    assert cube1.intersection(cube2)
    assert cube1.intersection(cube2).size == 36


def _main() -> str:
    my_input = load_lines()
    reactor = Reactor()
    for line in my_input:
        cuboid = Instruction.parse_input(line)
        reactor.apply_instruction(cuboid)
        print(cuboid)
    return str(reactor.count_on())


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
