import dataclasses
import inspect
import os
from typing import Optional, List


def find_input_filename(test: bool = False) -> Optional[str]:
    suffix = "-input.txt" if not test else "-test.txt"
    my_filename = __name__
    for frame in inspect.stack():
        filename, ext = os.path.basename(frame.filename).split(".", 1)
        if filename != my_filename:
            f_prefix = filename.split("-", 1)[0]
            return f"{f_prefix}{suffix}"
    raise FileExistsError("Could not find input file")


def load_input(input_file: Optional[str] = None, test: bool = False) -> str:
    input_file = input_file or find_input_filename(test)
    with open(input_file, "r") as f:
        return f.read().strip()


def load_lines(input_file: Optional[str] = None, test: bool = False) -> List[str]:
    return load_input(input_file, test).split("\n")


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
