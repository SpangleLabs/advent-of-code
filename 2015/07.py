from typing import Dict

from utils.input import load_lines_split
from utils.types import is_int

gate_lookup = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "NOT": lambda _, y: ~y,
    "LSHIFT": lambda x, y: x << y,
    "RSHIFT": lambda x, y: x >> y
}


def run_command(cmd_lookup: Dict[str, str], results_lookup: Dict[str, int], cmd: str) -> int:
    if cmd in results_lookup:
        return results_lookup[cmd]
    if " " not in cmd:
        if is_int(cmd):
            results_lookup[cmd] = int(cmd)
            return int(cmd)
        else:
            return run_command(cmd_lookup, results_lookup, cmd_lookup[cmd])
    cmd_args = cmd.split()
    if len(cmd_args) == 2:
        cmd_args = [None, *cmd_args]
    cmd_x = cmd_args[0]
    if cmd_x is not None:
        cmd_x = run_command(cmd_lookup, results_lookup, cmd_x)
    else:
        cmd_x = lambda: None
    cmd_y = cmd_args[2]
    if is_int(cmd_y):
        cmd_y = int(cmd_y)
    else:
        cmd_y = run_command(cmd_lookup, results_lookup, cmd_y)
    result = gate_lookup[cmd_args[1]](cmd_x, cmd_y) % 2 ** 16
    results_lookup[cmd] = result
    return result


if __name__ == "__main__":
    cmds_dict = {}
    for src, target in load_lines_split(" -> "):
        cmds_dict[target] = src
    results_dict = {}
    for key in cmds_dict.keys():
        print(f"{key}: {run_command(cmds_dict, results_dict, key)}")
    print(run_command(cmds_dict, results_dict, "a"))
