import datetime
import math
from typing import Tuple

from utils.coords2d import Coords2D
from utils.input import load_input
from utils.math import triangle_number


def parse_target(input_str: str) -> Tuple[Coords2D, Coords2D]:
    _, target = input_str.split(": ")
    x_target, y_target = target.split(", ")
    if x_target.startswith("y="):
        x_target, y_target = y_target, x_target
    x_bounds = [int(x) for x in x_target.lstrip("x=").split("..")]
    y_bounds = [int(y) for y in y_target.lstrip("y=").split("..")]
    return Coords2D(min(x_bounds), max(y_bounds)), Coords2D(max(x_bounds), min(y_bounds))


def position_after_step(start_velocity: Coords2D, step: int) -> Coords2D:
    if step > start_velocity.x:
        x_val = triangle_number(start_velocity.x)
    else:
        x_diff = start_velocity.x - step
        x_val = (step * x_diff) + triangle_number(step)
    y_val = (start_velocity.y * step) - triangle_number(step - 1)
    return Coords2D(x_val, y_val)


def reverse_triangle(triangle: int) -> int:
    return math.floor(math.sqrt(2 * triangle)) - 1


def _main() -> str:
    my_input = load_input()
    target_start, target_end = parse_target(my_input)
    max_x = target_end.x
    min_x = reverse_triangle(target_start.x)
    min_y = target_end.y
    # After start_vel_y * 2 +1 steps, y will be zero, then it will drop by -y - 1
    # So maximum y is such that target_end.y > -y -1
    max_y = -target_end.y + 1
    max_max_height = 0
    max_vel = None
    workable_velocities = set()
    print(f"Y range: {min_y}, {max_y}")
    print(f"X range: {min_x}, {max_x}")
    for try_y in range(min_y, max_y + 1):
        for try_x in range(min_x, max_x + 1):
            try_vel = Coords2D(try_x, try_y)
            # print(try_vel)
            # max_height = 0
            step = 1
            out_of_bounds = False
            landed_in_target = False
            while not out_of_bounds and not landed_in_target:
                pos = position_after_step(try_vel, step)
                # max_height = max(max_height or 0, pos.y)
                if pos.x > target_end.x or pos.y < target_end.y:
                    out_of_bounds = True
                if target_start.x <= pos.x <= target_end.x and target_start.y >= pos.y >= target_end.y:
                    print(f"Landed on target! {try_vel}")
                    landed_in_target = True
                    workable_velocities.add(try_vel)
                step += 1
    return str(len(workable_velocities))


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
