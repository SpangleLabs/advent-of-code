from abc import ABC, abstractmethod
import dataclasses
import datetime
import itertools
from functools import cached_property
from typing import List, Tuple, Set, Optional
import numpy

from utils.coords3d import Coords3D
from utils.input import load_input


class Transformation3D(ABC):

    @property
    @abstractmethod
    def matrix(self) -> numpy.array:
        raise NotImplementedError

    @abstractmethod
    def apply_transformation(self, coord: Coords3D) -> Coords3D:
        raise NotImplementedError

    @abstractmethod
    def __neg__(self) -> "Transformation3D":
        raise NotImplementedError


@dataclasses.dataclass(eq=True, frozen=True)
class Flip3D(Transformation3D):
    coord_flip: int

    @property
    def matrix(self) -> numpy.array:
        return numpy.array([
            [(2 * (self.coord_flip % 2)) - 1, 0, 0, 0],
            [0, (2 * (self.coord_flip // 2 % 2)) - 1, 0, 0],
            [0, 0, (2 * (self.coord_flip // 4 % 2)) - 1, 0],
            [0, 0, 0, 1]
        ])

    def apply_transformation(self, coord: Coords3D) -> Coords3D:
        x_flip = (2 * (self.coord_flip % 2)) - 1
        y_flip = (2 * (self.coord_flip // 2 % 2)) - 1
        z_flip = (2 * (self.coord_flip // 4 % 2)) - 1
        return Coords3D(
            x_flip * coord.x,
            y_flip * coord.y,
            z_flip * coord.z
        )

    def __neg__(self) -> "Flip3D":
        return Flip3D(
            self.coord_flip
        )


@dataclasses.dataclass(eq=True, frozen=True)
class Rotation3D(Transformation3D):
    coord_order: str

    @property
    def matrix(self) -> numpy.array:
        char1 = self.coord_order[0]
        char2 = self.coord_order[1]
        char3 = self.coord_order[2]
        return numpy.array([
            [int("x" == char1), int("y" == char1), int("z" == char1), 0],
            [int("x" == char2), int("y" == char2), int("z" == char2), 0],
            [int("x" == char3), int("y" == char3), int("z" == char3), 0],
            [0, 0, 0, 1]
        ])

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
class Translate3D(Transformation3D):
    coord: Coords3D

    @property
    def matrix(self) -> numpy.array:
        return numpy.array([
            [1, 0, 0, self.coord.x],
            [0, 1, 0, self.coord.y],
            [0, 0, 1, self.coord.z],
            [0, 0, 0, 1]
        ])

    def apply_transformation(self, coord: Coords3D) -> Coords3D:
        return coord + self.coord

    def __neg__(self) -> "Translate3D":
        return Translate3D(-self.coord)


@dataclasses.dataclass(eq=True, frozen=True)
class CompoundTransformation:
    transformations: Tuple[Transformation3D, ...]

    @cached_property
    def matrix(self) -> numpy.array:
        result = numpy.identity(4)
        for trans in self.transformations[::-1]:
            result = numpy.matmul(result, trans.matrix)
        return result

    def apply(self, coords: Coords3D) -> Coords3D:
        coord_array = numpy.array([coords.x, coords.y, coords.z, 1])
        result = numpy.matmul(self.matrix, coord_array)
        return Coords3D(result[0], result[1], result[2])

    def __neg__(self) -> "CompoundTransformation":
        transformations: List[Transformation3D] = []
        for trans in self.transformations[::-1]:
            transformations.append(-trans)
        return CompoundTransformation(tuple(transformations))


def transform_beacons(beacons: Set[Coords3D], transformation: CompoundTransformation) -> Set[Coords3D]:
    return {
        transformation.apply(beacon)
        for beacon in beacons
    }


def all_transformations() -> List[Tuple[Rotation3D, Flip3D]]:
    results = []
    for coord_order in itertools.permutations("xyz", 3):
        for coord_flip in range(8):
            rotation = Rotation3D("".join(coord_order))
            flip = Flip3D(coord_flip)
            results.append((rotation, flip))
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
                for rotate, flip in all_transformations():
                    compound_tf = CompoundTransformation(
                        (
                            Translate3D(-my_beacon),
                            rotate,
                            flip,
                            Translate3D(their_beacon)
                        )
                    )
                    my_mapped_beacons = transform_beacons(self.beacons, compound_tf)

                    my_intersect_beacons = my_mapped_beacons.intersection(other.beacons)
                    if len(my_intersect_beacons) < 12:
                        continue
                    else:
                        return CompoundTransformation(
                            (
                                Translate3D(-my_beacon),
                                rotate,
                                flip,
                                Translate3D(their_beacon)
                            )
                        )

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


def _test() -> None:
    coord = Coords3D(123, 456, 789)
    translate = Translate3D(Coords3D(64, 32, 79))
    for rotate, flip in all_transformations():

        compound_translate = CompoundTransformation((translate,))
        compound_rotate = CompoundTransformation((rotate,))
        compound_flip = CompoundTransformation((flip,))
        assert translate.apply_transformation(coord) == compound_translate.apply(coord)
        assert rotate.apply_transformation(coord) == compound_rotate.apply(coord)
        assert flip.apply_transformation(coord) == compound_flip.apply(coord)

        compound_full = CompoundTransformation((translate, rotate, flip, -translate))
        coords_full = translate.apply_transformation(coord)
        coords_full = rotate.apply_transformation(coords_full)
        coords_full = flip.apply_transformation(coords_full)
        coords_full = (-translate).apply_transformation(coords_full)
        assert coords_full == compound_full.apply(coord)


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
    # Gather all coordinates
    all_coords = scanners[0].beacons
    for scanner in scanners[1:]:
        zeroed_coords = scanner.beacons
        for tf in scanner.transforms[::-1]:
            zeroed_coords = transform_beacons(zeroed_coords, -tf)
        all_coords = all_coords.union(zeroed_coords)
    return str(len(all_coords))


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
