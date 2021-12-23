import datetime
from typing import List

from utils.coords2d import Map2D, Coords2D
from utils.input import load_input


class InfiniteImage(Map2D[bool]):

    def __init__(self, width: int, height: int, fill: bool = False, off_side: bool = False):
        super().__init__(width, height, fill=fill)
        self.off_side = off_side

    def render(self) -> str:
        return "\n".join(
            "".join("#" if char else "." for char in line)
            for line in self.map
        )


def coords_to_binary_num(img: InfiniteImage, coords: List[Coords2D]) -> int:
    coords = sorted(coords, key=lambda c: (c.y, c.x))
    return int("".join(str(int(not not img.try_get_value(c, img.off_side))) for c in coords), 2)


def enhance(image: InfiniteImage, lookup: str) -> InfiniteImage:
    new_off_side = lookup[0] == "#"
    if image.off_side:
        new_off_side = lookup[9] == "#"
    new_image = InfiniteImage(image.width + 2, image.height + 2, off_side=new_off_side)
    offset = Coords2D(1, 1)
    for coord in new_image.all_coords():
        old_coord = coord - offset
        neighbours = old_coord.list_neighbours(True) + [old_coord]
        binary = coords_to_binary_num(image, neighbours)
        if lookup[binary] == "#":
            new_image.set_value(coord, True)
    return new_image


def _test() -> None:
    m = InfiniteImage.from_bool_input([
        "...",
        "#..",
        ".#."
    ], "#")
    lookup = "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#"
    binary = coords_to_binary_num(m, m.all_coords())
    assert binary == 34
    assert lookup[binary] == "#"


def _main() -> str:
    scale_factor, image = load_input().split("\n\n")
    image = InfiniteImage.from_bool_input(image.split("\n"), "#")
    for step in range(2):
        image = enhance(image, scale_factor)
        print(image.render())
    return str(image.count(True))


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
