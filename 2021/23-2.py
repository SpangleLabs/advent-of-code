import datetime
from enum import Enum
from typing import List, Optional

from utils.input import load_lines
from utils.math import triangle_number


class AmphipodSpecies(Enum):
    Amber = 1
    Bronze = 10
    Copper = 100
    Desert = 1000


class Amphipod:
    def __init__(self, species: AmphipodSpecies, location: int, depth: int) -> None:
        self.species = species
        self.location = location
        self.depth = depth
        self.cost = 0

    def add_movement_cost(self, moves: int) -> None:
        self.cost += abs(moves) * self.species.value

    def move_to_hallway(self, location: int) -> None:
        print(f"Moving {self.species} from {self.location},{self.depth} to {location},0")
        self.add_movement_cost(self.depth)
        self.depth = 0
        self.add_movement_cost(location - self.location)
        self.location = location

    def move_down(self, depth: int) -> None:
        print(f"Moving {self.species} down {depth}")
        self.add_movement_cost(depth)
        self.depth = depth

    @property
    def target_location(self) -> int:
        return {
            AmphipodSpecies.Amber: 2,
            AmphipodSpecies.Bronze: 4,
            AmphipodSpecies.Copper: 6,
            AmphipodSpecies.Desert: 8
        }[self.species]

    @classmethod
    def from_letter(cls, letter: str, location: int, depth: int) -> "Amphipod":
        return cls(
            {
                "A": AmphipodSpecies.Amber,
                "B": AmphipodSpecies.Bronze,
                "C": AmphipodSpecies.Copper,
                "D": AmphipodSpecies.Desert
            }[letter],
            location,
            depth
        )

    def is_home(self, others: List["Amphipod"]) -> bool:
        if self.location != self.target_location:
            return False
        for other in others:
            if other.location == self.location:
                if other.species != self.species:
                    if other.depth > self.depth:
                        return False
        return True


class Room:
    def __init__(self, location: int, top: Amphipod, bottom: Amphipod, intended_species: AmphipodSpecies) -> None:
        self.location = location
        self.top = top
        self.bottom = bottom
        self.intended_species = intended_species


class Burrow:

    def __init__(self, amphipods: List[Amphipod], cost: int):
        self.hallway = {
            0: "",
            1: "",
            3: "",
            5: "",
            7: "",
            9: "",
            10: ""
        }
        self.amphipods = amphipods
        self.cost = cost
        self.a_locations = [1, 9, 0, 10]
        self.b_locations = [3, 7]

    @classmethod
    def parse_input(cls, input_data: List[str]) -> "Burrow":
        input_data = input_data[:3] + ["#D#C#B#A#", "#D#B#A#C#"] + input_data[3:]
        amphi_rows = [
            line.strip().replace("#", "")
            for line in input_data[2:]
        ]
        amphipods = sum([
            [
                Amphipod.from_letter(char, i * 2, depth)
                for i, char in enumerate(row, start=1)
            ] for depth, row in enumerate(amphi_rows, start=1)
        ], start=[])
        return cls(amphipods, 0)

    def target_room_ready(self, room_loc: int) -> bool:
        return not any(
            amphipod.location == room_loc and amphipod.target_location != room_loc
            for amphipod in self.amphipods
        )

    def game_complete(self) -> bool:
        return all(
            amphipod.target_location == amphipod.location for amphipod in self.amphipods
        )
    
    def minimum_solution_cost(self) -> int:
        total_cost = 0
        for amphipod in self.amphipods:
            if amphipod.is_home(self.amphipods):
                print(f"Already home: {amphipod.species}")
                continue
            total_cost += amphipod.depth * amphipod.species.value
            total_cost += abs(amphipod.location - amphipod.target_location) * amphipod.species.value
        for species in AmphipodSpecies:
            displaced_amphipods = sum(
                1
                for a in self.amphipods
                if a.species == species and not a.is_home(self.amphipods)
            )
            total_cost += triangle_number(displaced_amphipods) * species.value
        return total_cost

    def amphipod_at_location(self, location: int, depth: int) -> Optional[Amphipod]:
        return next(
            (a for a in self.amphipods if a.location == location and a.depth == depth),
            None
        )

    def render(self) -> str:
        hallway = [
            [
                self.amphipod_at_location(x, d) if d == 0 or x in [2, 4, 6, 8] else "#"
                for x in range(11)
            ] for d in range(5)
        ]
        lines = [
            "".join([
                "_" if a is None else (a.species.name[0] if isinstance(a, Amphipod) else a)
                for a in line
            ])
            for line in hallway
        ]
        return "\n".join(lines)

    def next_a_location(self) -> Optional[int]:
        for loc in self.a_locations:
            if self.amphipod_at_location(loc, 0):
                continue
            return loc
        raise NotImplemented("Out of A locations")

    def move_to_a_location(self, amphipod: Amphipod):
        new_location = self.next_a_location()
        amphipod.move_to_hallway(new_location)

    def move_to_left_a_location(self, amphipod: Amphipod):
        for loc in [0, 1, 9, 10]:
            if self.amphipod_at_location(loc, 0):
                continue
            amphipod.move_to_hallway(loc)
            return
        raise NotImplemented("Out of A locations")

    def move_to_b_location(self, amphipod: Amphipod):
        for loc in self.b_locations:
            if self.amphipod_at_location(loc, 0):
                continue
            amphipod.move_to_hallway(loc)
            return
        for loc in self.a_locations:
            if a := self.amphipod_at_location(loc, 0):
                if a.species == AmphipodSpecies.Amber:
                    if a.location < 5:
                        next_a_loc = a.location - 1
                    else:
                        next_a_loc = a.location + 1
                    a.move_to_hallway(next_a_loc)
                    amphipod.move_to_hallway(loc)
                    return
            else:
                amphipod.move_to_hallway(loc)
                return
        raise NotImplemented("Out of B locations")


def amphipods_in_room(burrow: Burrow, room_loc: int) -> List[Amphipod]:
    return sorted(
        [a for a in burrow.amphipods if a.location == room_loc and not a.is_home(burrow.amphipods)],
        key=lambda a: a.depth
    )


def hallway_amphipods_species(burrow: Burrow, species: AmphipodSpecies) -> List[Amphipod]:
    return [a for a in burrow.amphipods if a.depth == 0 and a.species == species]


def solve(burrow: Burrow) -> int:
    # min_cost = burrow.minimum_solution_cost()
    # Clear room C
    print("Clear room C")
    room_c = amphipods_in_room(burrow, 6)
    # # Moving A out of the way of D-home
    # # Keeping B close to Chome
    for a in room_c:
        if a.species == AmphipodSpecies.Amber:
            burrow.move_to_left_a_location(a)
        if a.species in [AmphipodSpecies.Bronze, AmphipodSpecies.Copper]:
            burrow.move_to_b_location(a)
        if a.species == AmphipodSpecies.Desert:
            print("Dunno lol")
            raise NotImplemented("Not sure")
    print(burrow.render())
    # Clear room B
    print("Clear room B")
    room_b = amphipods_in_room(burrow, 4)
    room_c_depth = len(room_c)
    d_locations = [7]
    for a in room_b:
        if a.species == AmphipodSpecies.Copper:
            a.move_to_hallway(6)
            a.move_down(room_c_depth)
            room_c_depth -= 1
        if a.species == AmphipodSpecies.Bronze:
            burrow.move_to_b_location(a)
        if a.species == AmphipodSpecies.Amber:
            burrow.move_to_a_location(a)
        if a.species == AmphipodSpecies.Desert:
            new_location = d_locations.pop(0)
            a.move_to_hallway(new_location)
    print(burrow.render())
    # Put all of C into home
    print("Move C to home")
    c_amphipods = hallway_amphipods_species(burrow, AmphipodSpecies.Copper)
    for a in c_amphipods:
        a.move_to_hallway(6)
        a.move_down(room_c_depth)
        room_c_depth -= 1
    print(burrow.render())
    # Get all of B into home
    print("Move B to home")
    b_amphipods = hallway_amphipods_species(burrow, AmphipodSpecies.Bronze)
    room_b_depth = len(room_b)
    for a in b_amphipods:
        a.move_to_hallway(4)
        a.move_down(room_b_depth)
        room_b_depth -= 1
    print(burrow.render())
    # Clear room D
    print("Clear room D")
    room_d = amphipods_in_room(burrow, 8)
    d_locations = [7, 9, 5, 3]
    for a in room_d:
        if a.species == AmphipodSpecies.Amber:
            burrow.move_to_a_location(a)
        if a.species == AmphipodSpecies.Bronze:
            a.move_to_hallway(4)
            a.move_down(room_b_depth)
            room_b_depth -= 1
        if a.species == AmphipodSpecies.Copper:
            a.move_to_hallway(6)
            a.move_down(room_c_depth)
            room_c_depth -= 1
        if a.species == AmphipodSpecies.Desert:
            new_location = d_locations.pop(0)
            a.move_to_hallway(new_location)
    print(burrow.render())
    # Clear room A
    print("Clear room A")
    room_a = amphipods_in_room(burrow, 2)
    room_d_depth = len(room_d)
    for a in room_a:
        if a.species == AmphipodSpecies.Amber:
            burrow.move_to_a_location(a)
        if a.species == AmphipodSpecies.Bronze:
            a.move_to_hallway(4)
            a.move_down(room_b_depth)
            room_b_depth -= 1
        if a.species == AmphipodSpecies.Copper:
            a.move_to_hallway(6)
            a.move_down(room_c_depth)
            room_c_depth -= 1
        if a.species == AmphipodSpecies.Desert:
            a.move_to_hallway(8)
            a.move_down(room_d_depth)
            room_d_depth -= 1
    print(burrow.render())
    # Move all D into D
    print("Move D to home")
    d_amphipods = hallway_amphipods_species(burrow, AmphipodSpecies.Desert)
    for a in d_amphipods:
        a.move_to_hallway(8)
        a.move_down(room_d_depth)
        room_d_depth -= 1
    print(burrow.render())
    # Move A into A
    print("Move A to home")
    a_amphipods = hallway_amphipods_species(burrow, AmphipodSpecies.Amber)
    room_a_depth = len(room_a)
    for a in a_amphipods:
        a.move_to_hallway(2)
        a.move_down(room_a_depth)
        room_a_depth -= 1
    print(burrow.render())
    for a in burrow.amphipods:
        print(f"{a.species}: {a.cost}")
    return sum(a.cost for a in burrow.amphipods)


def _main() -> str:
    my_input = load_lines()
    burrow = Burrow.parse_input(my_input)
    print(burrow.render())
    min_cost = burrow.minimum_solution_cost()
    print(f"Minimum solution cost, if amphipods could pass through each-other, is: {min_cost}")
    return str(solve(burrow))


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
