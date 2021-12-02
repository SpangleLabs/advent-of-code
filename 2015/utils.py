import inspect
import os
from typing import Optional, List


def find_input_filename() -> Optional[str]:
    my_filename = __name__
    for frame in inspect.stack():
        filename, ext = os.path.basename(frame.filename).split(".", 1)
        if filename != my_filename:
            f_prefix = filename.split("-", 1)[0]
            return f"{f_prefix}-input.txt"
    raise FileExistsError("Could not find input file")


def load_input(input_file: Optional[str] = None) -> str:
    input_file = input_file or find_input_filename()
    with open(input_file, "r") as f:
        return f.read().strip()


def load_lines(input_file: Optional[str] = None) -> List[str]:
    return load_input(input_file).split("\n")
