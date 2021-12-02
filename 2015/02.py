from utils import load_lines


def parcel_area(l: int, w: int, h: int) -> int:
    surface = 2*(l*h + h*w + l*w)
    sides = [l, w, h]
    sides.remove(max(sides))
    slack = sides[0] * sides[1]
    return surface + slack


if __name__ == "__main__":
    total_area = 0
    parcels = [line.split("x") for line in load_lines()]
    for l, w, h in parcels:
        total_area += parcel_area(int(l), int(w), int(h))
    print(total_area)
