import dataclasses


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
