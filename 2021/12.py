from collections import defaultdict
from typing import List, Dict, Set

from utils.input import load_lines


def is_valid_path(path: List[str]) -> bool:
    small_caves = [cave for cave in path if cave.islower()]
    return len(small_caves) == len(set(small_caves))


def is_complete_path(path: List[str]) -> bool:
    return path[0] == "start" and path[-1] == "end"


def find_paths(links: Dict[str, Set[str]], start_path: List[str]) -> List[List[str]]:
    if is_complete_path(start_path):
        return []
    paths = []
    last_cave = start_path[-1]
    for next_cave in links[last_cave]:
        if is_valid_path(start_path + [next_cave]):
            paths.append(start_path + [next_cave])
    return paths


def find_all_paths(links: Dict[str, Set[str]]) -> List[List[str]]:
    paths = []
    new_paths = find_paths(link_map, ["start"])
    while True:
        try_next = []
        for path in new_paths:
            found = find_paths(links, path)
            if found:
                try_next.extend(found)
                paths.extend([path for path in found if is_complete_path(path)])
        if not try_next:
            return paths
        new_paths = try_next


if __name__ == "__main__":
    my_input = load_lines()
    link_map = defaultdict(lambda: set())
    for line in my_input:
        start, end = line.split("-")
        link_map[start].add(end)
        link_map[end].add(start)
    total_paths = find_all_paths(link_map)
    for p in total_paths:
        print(p)
    print(len(total_paths))
