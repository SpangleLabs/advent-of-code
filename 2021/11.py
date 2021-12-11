from typing import List

from utils.coords2d import Map2D, Coords2D
from utils.input import load_lines


class OctopodeGrid:
    def __init__(self, input_lines: List[str]) -> None:
        self.energy = Map2D.from_number_input(input_lines)
        self.flashed = Map2D(self.energy.width, self.energy.height)

    def increase_energy_everywhere(self) -> None:
        for coord in self.energy.all_coords():
            self.increase_energy(coord)

    def increase_energy(self, coords: Coords2D) -> None:
        self.energy.set_value(coords, self.energy.get_value(coords) + 1)

    def list_flashes(self) -> List[Coords2D]:
        flashes = []
        for coord in self.energy.all_coords():
            if self.energy.get_value(coord) > 9 and not self.flashed.get_value(coord):
                flashes.append(coord)
        return flashes

    def mark_flashed(self, coords: Coords2D) -> None:
        self.flashed.set_value(coords, True)

    def increase_neighbours(self, coords: Coords2D) -> None:
        for coord in self.energy.valid_neighbours(coords, True):
            if not self.flashed.get_value(coord):
                self.increase_energy(coord)

    def flashes(self) -> int:
        flashes = 0
        while True:
            new_flashes = self.list_flashes()
            if not new_flashes:
                return flashes
            for flash in new_flashes:
                self.mark_flashed(flash)
                self.increase_neighbours(flash)
                flashes += 1

    def reset_flashes(self) -> None:
        self.flashed = Map2D(self.flashed.width, self.flashed.height, False)
        for coord in self.energy.all_coords():
            if self.energy.get_value(coord) > 9:
                self.energy.set_value(coord, 0)

    def render(self) -> str:
        return "\n".join(
            "".join(str(x) for x in row)
            for row in self.energy.map
        )


if __name__ == "__main__":
    oct = OctopodeGrid(load_lines())
    total = 0
    for step in range(100):
        oct.increase_energy_everywhere()
        total += oct.flashes()
        oct.reset_flashes()
        print("-")
        print(f"After step {step}")
        print(oct.render())
    print(total)
