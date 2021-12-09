from typing import List

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


if __name__ == "__main__":
    grid = Grid(load_lines())
    low_points = []
    for coords in grid.all_coords():
        next = grid.find_neighbours(coords)
        if grid.get_value(coords) < min(grid.get_value(n) for n in next):
            low_points.append(coords)
    print(sum(grid.get_value(l) + 1 for l in low_points))
