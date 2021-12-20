import dataclasses
import datetime
import itertools
from typing import List, Dict, Tuple, Set, Optional

from utils.coords3d import Coords3D
from utils.input import load_input


@dataclasses.dataclass(eq=True, frozen=True)
class Rotation3D:
    coord_order: str
    coord_flip: int

    def rotate_coord(self, coord: Coords3D) -> Coords3D:
        x_flip = (2 * (self.coord_flip % 2)) - 1
        y_flip = (2 * (self.coord_flip // 2 % 2)) - 1
        z_flip = (2 * (self.coord_flip // 4 % 2)) - 1
        return Coords3D(
            x_flip * coord.__getattribute__(self.coord_order[0]),
            y_flip * coord.__getattribute__(self.coord_order[1]),
            z_flip * coord.__getattribute__(self.coord_order[2])
        )

    def __neg__(self) -> "Rotation3D":
        new_order = {
            "xyz": "xyz",
            "xzy": "xzy",
            "yxz": "yxz",
            "yzx": "zxy",
            "zxy": "yzx",
            "zyx": "zyx",
        }[self.coord_order]
        flips = {
            "x": str((self.coord_flip % 2)),
            "y": str((self.coord_flip // 2 % 2)),
            "z": str((self.coord_flip // 4 % 2))
        }
        new_flip = int("".join(flips[axis] for axis in new_order[::-1]), base=2)
        return Rotation3D(new_order, new_flip)


def translate_beacons(beacons: Set[Coords3D], translation: Coords3D) -> Set[Coords3D]:
    return {
        beacon + translation
        for beacon in beacons
    }


def rotate_beacons(beacons: Set[Coords3D], rotation: Rotation3D) -> Set[Coords3D]:
    return {
        rotation.rotate_coord(beacon)
        for beacon in beacons
    }


def all_rotations(beacons: Set[Coords3D]) -> Dict[Rotation3D, Set[Coords3D]]:
    results = {}
    for coord_order in itertools.permutations("xyz", 3):
        for coord_flip in range(8):
            rotation = Rotation3D("".join(coord_order), coord_flip)
            results[rotation] = rotate_beacons(beacons, rotation)
    return results


def truncate_beacons(beacons: Set[Coords3D], max_distance: int = 1000) -> Set[Coords3D]:
    return {
        beacon
        for beacon in beacons
        if all([
            -max_distance <= beacon.x <= max_distance,
            -max_distance <= beacon.y <= max_distance,
            -max_distance <= beacon.z <= max_distance
        ])
    }


class Scanner:
    def __init__(self, number: int, beacons: Set[Coords3D], offsets: List[Tuple[Coords3D, Rotation3D]] = None) -> None:
        self.number = number
        self.beacons = beacons
        self.offsets = offsets

    @classmethod
    def parse_input(cls, scanner_lines: List[str]) -> "Scanner":
        number = int(scanner_lines[0].strip(" -").split()[-1])
        coords = {
            Coords3D.from_input_line(line) for line in scanner_lines[1:]
        }
        return cls(number, coords)

    def overlap_point(self, other: "Scanner") -> Optional[Tuple[Coords3D, Rotation3D]]:
        for my_beacon in self.beacons:
            for their_beacon in other.beacons:
                my_beacons = translate_beacons(self.beacons, -my_beacon)
                for rotation, my_rotate_beacons in all_rotations(my_beacons).items():
                    my_mapped_beacons = translate_beacons(my_rotate_beacons, their_beacon)

                    my_intersect_beacons = my_mapped_beacons.intersection(other.beacons)
                    if len(my_intersect_beacons) < 12:
                        continue
                    else:
                        return my_beacon - rotation.rotate_coord(their_beacon), rotation

                    if False:
                        my_intersect_beacons = truncate_beacons(my_mapped_beacons)
                        if len(my_intersect_beacons) < 12:
                            continue
                        if not my_intersect_beacons.issubset(other.beacons):
                            continue

                        their_beacons = translate_beacons(other.beacons, -their_beacon)
                        their_rotate_beacons = rotate_beacons(their_beacons, -rotation)
                        their_mapped_beacons = translate_beacons(their_rotate_beacons, my_beacon)
                        their_intersect_beacons = truncate_beacons(their_mapped_beacons)
                        if len(their_intersect_beacons) < 12:
                            continue
                        if not their_intersect_beacons.issubset(self.beacons):
                            continue

                        print(f"Overlap between {self.number} and {other.number}. {len(my_intersect_beacons)}, {len(their_intersect_beacons)} beacons")
                        if len(my_intersect_beacons) == len(their_intersect_beacons):
                            return my_beacon - rotation.rotate_coord(their_beacon), rotation
                        print(f"NON EQUAL OVERLAP???")
        return None


def find_overlaps(scanners: List[Scanner]) -> None:
    unknown_scanners = [scanner for scanner in scanners if scanner.offsets is None]
    newly_known = [scanner for scanner in scanners if scanner.offsets is not None]
    while newly_known:
        print("Searching again")
        try_next = []
        for known_scanner in newly_known:
            for unknown_scanner in unknown_scanners:
                print(f"Checking {known_scanner.number} against {unknown_scanner.number}")
                if offset := known_scanner.overlap_point(unknown_scanner):
                    unknown_scanner.offsets = known_scanner.offsets + [offset]
                    print(f"Scanner {known_scanner.number} and {unknown_scanner.number} overlap!")
                    try_next.append(unknown_scanner)
        newly_known = try_next
        unknown_scanners = [scanner for scanner in scanners if scanner.offsets is None]


def _main() -> str:
    my_input = load_input(test=True)
    scanner_inputs = my_input.split("\n\n")
    # Parse scanners
    scanners = []
    for scanner_input in scanner_inputs:
        scanners.append(Scanner.parse_input(scanner_input.split("\n")))
    # scanners = scanners[:2]
    # coord = Coords3D(14, -230, 408)
    # rotate = Rotation3D("yzx", 2)
    # print(coord)
    # print(rotate)
    # print(rotate.rotate_coord(coord))
    # print(-rotate)
    # print((-rotate).rotate_coord(rotate.rotate_coord(coord)))


    # Find overlaps
    scanners[0].offsets = [(Coords3D(0, 0, 0), Rotation3D("xyz", 7))]
    find_overlaps(scanners)
    # Gather all coordinates
    all_coords = scanners[0].beacons
    for scanner in scanners[1:]:
        zeroed_coords = scanner.beacons
        for coords, rotation in scanner.offsets[::-1]:
            zeroed_coords = translate_beacons(zeroed_coords, (rotation).rotate_coord(coords))
            zeroed_coords = rotate_beacons(zeroed_coords, rotation)
        all_coords = all_coords.union(zeroed_coords)
    return str(len(all_coords))


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
