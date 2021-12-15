import datetime
from math import inf
from typing import List

from utils.coords2d import Map2D, Coords2D
from utils.input import load_lines


class RiskMap:
    def __init__(self, input_lines: List[str]):
        self.start = Coords2D(0, 0)
        self.risk = Map2D.from_number_input(input_lines)
        self.end = Coords2D(self.risk.width - 1, self.risk.height - 1)
        self.tentative_risk = Map2D(self.risk.width, self.risk.height, inf)
        self.tentative_risk.set_value(self.start, 0)
        self.total_risk = Map2D(self.risk.width, self.risk.height, None)
        self.total_risk.set_value(self.start, 0)
        self.tentative_coords = set()

    def calculate_distances(self) -> None:
        found = False
        current_node = self.start
        while not found:
            self.calculate_distances_from_coord(current_node)
            lowest = self.find_lowest_tentative_risk()
            self.tentative_coords.remove(lowest)
            self.total_risk.set_value(lowest, self.tentative_risk.get_value(lowest))
            if lowest == self.end:
                found = True
            # print(self.render_totals())
            print(lowest)
            current_node = lowest

    def calculate_distances_from_coord(self, coord: Coords2D) -> None:
        current_risk = self.total_risk.get_value(coord)
        for neighbour in self.risk.valid_neighbours(coord, False):
            if self.total_risk.get_value(neighbour) is not None:
                continue
            total_risk = current_risk + self.risk.get_value(neighbour)
            self.tentative_risk.set_value_if_smaller(neighbour, total_risk)
            self.tentative_coords.add(neighbour)

    def render_totals(self) -> str:
        return "\n".join(
            ",".join(str(val) for val in row)
            for row in self.total_risk.map
        )

    def find_lowest_tentative_risk(self) -> Coords2D:
        lowest = None
        lowest_val = inf
        for coord in self.tentative_coords:
            if self.tentative_risk.get_value(coord) == inf:
                continue
            if self.total_risk.get_value(coord) is not None:
                continue
            tentative_risk = self.tentative_risk.get_value(coord)
            if tentative_risk < lowest_val:
                lowest_val = tentative_risk
                lowest = coord
        return lowest


def _main() -> str:
    my_input = load_lines()
    risk = RiskMap(my_input)
    risk.calculate_distances()
    return risk.total_risk.get_value(risk.end)


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print("Time taken: {(datetime.datetime.now() - start_time).total_seconds()}")
