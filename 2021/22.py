import datetime

from utils.coords3d import Map3D, Coords3D
from utils.input import load_lines


class Cuboid:
    def __init__(self, start: Coords3D, end: Coords3D, state: bool) -> None:
        self.start = start
        self.end = end
        self.state = state

    @classmethod
    def parse_input(cls, line: str) -> "Cuboid":
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
        return f"Cuboid({self.start}, {self.end}, {self.state})"


class Reactor:

    def __init__(self):
        self.map = Map3D(101, 101, 101, False)
        self.offset = -50

    def apply_cuboid(self, cuboid: Cuboid) -> None:
        start = cuboid.start - Coords3D(self.offset, self.offset, self.offset)
        end = cuboid.end - Coords3D(self.offset, self.offset, self.offset)
        if not self.map.valid_coords(start) or not self.map.valid_coords(end):
            print(f"Skipping cuboid: {cuboid}")
            return
        print(f"Applying cuboid: {cuboid}")
        for x in range(start.x, end.x + 1):
            for y in range(start.y, end.y + 1):
                for z in range(start.z, end.z + 1):
                    self.map.set_value(Coords3D(x, y, z), cuboid.state)

    def count_on(self) -> int:
        return self.map.count(True)


def _main() -> str:
    my_input = load_lines()
    reactor = Reactor()
    for line in my_input:
        cuboid = Cuboid.parse_input(line)
        reactor.apply_cuboid(cuboid)
    return str(reactor.count_on())


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
