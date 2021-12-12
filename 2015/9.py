import itertools
from collections import defaultdict
from typing import Dict, List

from utils.input import load_lines


def build_distances_map(input_lines: List[str]) -> Dict[str, Dict[str, int]]:
    distances: Dict[str, Dict[str, int]] = defaultdict(lambda: {})
    for dist_line in input_lines:
        places, dist = dist_line.split(" = ")
        start, end = places.split(" to ")
        distances[start][end] = int(dist)
        distances[end][start] = int(dist)
    return distances


def total_distance(distances: Dict[str, Dict[str, int]], route: List[str]) -> int:
    total = 0
    for loc_from, loc_to in zip(route, route[1:]):
        total += distances[loc_from][loc_to]
    return total


if __name__ == "__main__":
    dist_map = build_distances_map(load_lines())
    locations = list(dist_map.keys())
    min_dist = None
    for order in itertools.permutations(locations, len(locations)):
        distance = total_distance(dist_map, order)
        if min_dist is None or distance < min_dist:
            min_dist = distance
    print(min_dist)
