from typing import List, Set

from utils.coords2d import Map2D, Coords2D
from utils.input import load_lines


class Grid(Map2D):
    def __init__(self, input_lines: List[str]):
        height = len(input_lines)
        width = len(input_lines[0])
        super().__init__(width, height)
        for y, row in enumerate(input_lines):
            for x, num in enumerate(row):
                self.map[x][y] = int(num)
        self.remaining = Map2D(width, height, True)

    def find_neighbours(self, coords: Coords2D) -> List[Coords2D]:
        neighbours = []
        if coords.x > 0:
            neighbours.append(coords.copy(x=coords.x - 1))
        if coords.y > 0:
            neighbours.append(coords.copy(y=coords.y - 1))
        if coords.x < self.width - 1:
            neighbours.append(coords.copy(x=coords.x + 1))
        if coords.y < self.height - 1:
            neighbours.append(coords.copy(y=coords.y + 1))
        return neighbours

    def is_remaining(self, coords: Coords2D) -> bool:
        return self.remaining.get_value(coords)

    def mark(self, coords: Coords2D) -> None:
        self.remaining.set_value(coords, False)


def find_lowest_points(grid: Grid) -> List[Coords2D]:
    low_points = []
    for coords in grid.all_coords():
        neighbours = grid.find_neighbours(coords)
        if grid.get_value(coords) < min(grid.get_value(n) for n in neighbours):
            low_points.append(coords)
    return low_points


def add_basin_points(
        grid: Grid,
        last_value: int,
        coords: Coords2D,
        basin: Set[Coords2D],
        not_in_basin: Set[Coords2D]
) -> None:
    if coords in not_in_basin:
        return
    if not grid.is_remaining(coords):
        not_in_basin.add(coords)
        return
    my_value = grid.get_value(coords)
    if my_value == 9:
        not_in_basin.add(coords)
        return
    if my_value < last_value:
        not_in_basin.add(coords)
    else:
        basin.add(coords)
        add_basin_points(grid, my_value, coords, basin, not_in_basin)


def find_basin_size(grid: Grid, lowest_point: Coords2D) -> int:
    print(f"Finding basin from {lowest_point.x}, {lowest_point.y}")
    basin = {lowest_point}
    new_cells = basin.copy()
    while True:
        try_next = set()
        for cell in new_cells:
            neighbours = grid.find_neighbours(cell)
            for neighbour in neighbours:
                if grid.is_remaining(neighbour):
                    if grid.get_value(neighbour) != 9:
                        if grid.get_value(neighbour) > grid.get_value(cell):
                            print(f"Adding {neighbour.x}, {neighbour.y}")
                            basin.add(neighbour)
                            grid.mark(neighbour)
                            try_next.add(neighbour)
        if not try_next:
            return len(basin)
        new_cells = try_next


def find_all_basin_sizes(grid: Grid) -> List[int]:
    lowest_points = find_lowest_points(g)
    basin_sizes = []
    for lowest_point in lowest_points:
        basin_sizes.append(find_basin_size(grid, lowest_point))
    return basin_sizes


if __name__ == "__main__":
    g = Grid(load_lines())
    sizes = find_all_basin_sizes(g)
    print(sizes)
    sorted_sizes = sorted(sizes, reverse=True)
    print(sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2])
