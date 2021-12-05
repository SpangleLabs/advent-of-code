from utils.input import load_lines


def parcel_area(l: int, w: int, h: int) -> int:
    surface = 2*(l*h + h*w + l*w)
    sides = [l, w, h]
    sides.remove(max(sides))
    slack = sides[0] * sides[1]
    return surface + slack


def parcel_ribbon_length(l: int, w: int, h: int) -> int:
    volume = l*h*w
    sides = [l, w, h]
    sides.remove(max(sides))
    wrap = sum(sides) * 2
    return volume + wrap


if __name__ == "__main__":
    total_length = 0
    parcels = [line.split("x") for line in load_lines()]
    for l, w, h in parcels:
        total_length += parcel_ribbon_length(int(l), int(w), int(h))
    print(total_length)
