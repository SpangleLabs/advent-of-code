from utils.input import load_lines_split
from utils.types import is_int

####
# Does not work, as it reaches a RecursionError, but basically implementing haskell in python, so keeping because it's funny
####

if __name__ == "__main__":
    values_dict = {}
    cmd_lookup = {
        "AND": lambda x, y: x & y,
        "OR": lambda x, y: x | y,
        "NOT": lambda _, y: ~y,
        "LSHIFT": lambda x, y: x << y,
        "RSHIFT": lambda x, y: x >> y
    }
    for src, target in load_lines_split(" -> "):
        if " " not in src:
            if is_int(src):
                values_dict[target] = lambda s=src: int(s)
            else:
                values_dict[target] = lambda s=src: values_dict.get(s)()
            continue
        cmd_args = src.split()
        if len(cmd_args) == 2:
            cmd_args = [None, *cmd_args]
        cmd_x = cmd_args[0]
        if cmd_x is not None:
            cmd_x = lambda x=cmd_x: values_dict.get(x)()
        else:
            cmd_x = lambda: None
        cmd_y = cmd_args[2]
        if is_int(cmd_y):
            cmd_y = lambda y=cmd_y: int(y)
        else:
            cmd_y = lambda y=cmd_y: values_dict.get(y)()
        values_dict[target] = lambda: cmd_lookup[cmd_args[1]](cmd_x(), cmd_y()) % 2 ** 16
    print(values_dict)
    print(values_dict["a"]())
