from abc import ABC, abstractmethod
import dataclasses
import datetime
import itertools
from typing import List, Dict, Tuple, Set, Optional

from utils.coords3d import Coords3D
from utils.input import load_input


class Transformation3D(ABC):

    @abstractmethod
    def apply_transformation(self, coord: Coords3D) -> Coords3D:
        raise NotImplementedError

    @abstractmethod
    def __neg__(self) -> "Transformation3D":
        raise NotImplementedError


@dataclasses.dataclass(eq=True, frozen=True)
class Flip3D(Transformation3D):
    coord_flip: int

    def apply_transformation(self, coord: Coords3D) -> Coords3D:
        x_flip = (2 * (self.coord_flip % 2)) - 1
        y_flip = (2 * (self.coord_flip // 2 % 2)) - 1
        z_flip = (2 * (self.coord_flip // 4 % 2)) - 1
        return Coords3D(
            x_flip * coord.x,
            y_flip * coord.y,
            z_flip * coord.z
        )

    def __neg__(self) -> "Rotation3D":
        return Flip3D(
            self.coord_flip
        )


@dataclasses.dataclass(eq=True, frozen=True)
class Rotation3D(Transformation3D):
    coord_order: str

    def apply_transformation(self, coord: Coords3D) -> Coords3D:
        return Coords3D(
            coord.__getattribute__(self.coord_order[0]),
            coord.__getattribute__(self.coord_order[1]),
            coord.__getattribute__(self.coord_order[2])
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
        return Rotation3D(new_order)


@dataclasses.dataclass(eq=True, frozen=True)
class Translate3D:
    coord: Coords3D

    def apply_transformation(self, coord: Coords3D) -> Coords3D:
        return coord + self.coord

    def __neg__(self) -> Coords3D:
        return Translate3D(-self.coord)


@dataclasses.dataclass(eq=True, frozen=True)
class CompoundTransformation:
    transformations: Tuple[Transformation3D]

    def apply(self, coords: Coords3D) -> Coords3D:
        for trans in self.transformations:
            coords = trans.apply_transformation(coords)
        return coords

    def __neg__(self) -> "CompoundTransformation":
        transformations = []
        for trans in self.transformations[::-1]:
            transformations.append(-trans)
        return CompoundTransformation(tuple(transformations))


def translate_beacons(beacons: Set[Coords3D], translation: Coords3D) -> Set[Coords3D]:
    return {
        beacon + translation
        for beacon in beacons
    }


def transform_beacons(beacons: Set[Coords3D], transformation: CompoundTransformation) -> Set[Coords3D]:
    return {
        transformation.apply(beacon)
        for beacon in beacons
    }


def all_transformations(beacons: Set[Coords3D]) -> Dict[CompoundTransformation, Set[Coords3D]]:
    results = {}
    for coord_order in itertools.permutations("xyz", 3):
        for coord_flip in range(8):
            rotation = Rotation3D("".join(coord_order))
            flip = Flip3D(coord_flip)
            transformation = CompoundTransformation((rotation, flip))
            results[transformation] = transform_beacons(beacons, transformation)
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
    def __init__(self, number: int, beacons: Set[Coords3D], transforms: List[CompoundTransformation] = None) -> None:
        self.number = number
        self.beacons = beacons
        self.transforms = transforms

    @classmethod
    def parse_input(cls, scanner_lines: List[str]) -> "Scanner":
        number = int(scanner_lines[0].strip(" -").split()[-1])
        coords = {
            Coords3D.from_input_line(line) for line in scanner_lines[1:]
        }
        return cls(number, coords)

    def __eq__(self, other: "Scanner") -> bool:
        return self.number == other.number

    def __hash__(self) -> int:
        return hash((Scanner, self.number))

    def overlap_point(self, other: "Scanner") -> Optional[CompoundTransformation]:
        for my_beacon in self.beacons:
            for their_beacon in other.beacons:
                my_beacons = translate_beacons(self.beacons, -my_beacon)
                for transformation, my_transform_beacons in all_transformations(my_beacons).items():
                    my_mapped_beacons = translate_beacons(my_transform_beacons, their_beacon)

                    my_intersect_beacons = my_mapped_beacons.intersection(other.beacons)
                    if len(my_intersect_beacons) < 12:
                        continue
                    else:
                        return CompoundTransformation(
                            (
                                Translate3D(-my_beacon),
                                *transformation.transformations,
                                Translate3D(their_beacon)
                            )
                        )

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
    unknown_scanners = [scanner for scanner in scanners if scanner.transforms is None]
    newly_known = {scanner for scanner in scanners if scanner.transforms is not None}
    while newly_known:
        print("Searching again")
        try_next = set()
        for known_scanner in newly_known:
            for unknown_scanner in unknown_scanners:
                if unknown_scanner in try_next:
                    continue
                print(f"Checking {known_scanner.number} against {unknown_scanner.number}")
                if transform := known_scanner.overlap_point(unknown_scanner):
                    unknown_scanner.transforms = known_scanner.transforms + [transform]
                    print(f"Scanner {known_scanner.number} and {unknown_scanner.number} overlap!")
                    try_next.add(unknown_scanner)
        newly_known = try_next
        unknown_scanners = [scanner for scanner in scanners if scanner.transforms is None]


def _main() -> str:
    my_input = load_input()
    scanner_inputs = my_input.split("\n\n")
    # Parse scanners
    scanners = []
    for scanner_input in scanner_inputs:
        scanners.append(Scanner.parse_input(scanner_input.split("\n")))
    # scanners = scanners[:2]
    # coord = Coords3D(14, -230, 408)
    # for tf, coords in all_transformations(set([coord])).items():
    #     print(coord)
    #     print(tf.apply(coord))
    #     print((-tf).apply(tf.apply(coord)))
    #     assert coord == (-tf).apply(tf.apply(coord))
    # return


    # Find overlaps
    scanners[0].transforms = []
    find_overlaps(scanners)
    # Find scanner coords
    scanner_coords = {}
    for scanner in scanners:
        coords = Coords3D(0,0,0)
        for tf in scanner.transforms[::-1]:
            coords = (-tf).apply(coords)
        scanner_coords[scanner.number] = coords
    # Get all diffs
    distances = []
    for coords1 in scanner_coords.values():
        for coords2 in scanner_coords.values():
            distances.append(coords1.manhatten_distance(coords2))
    return str(max(distances))


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
