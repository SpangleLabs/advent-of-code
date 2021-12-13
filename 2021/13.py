from utils.coords2d import Map2D, Coords2D
from utils.input import load_input


class OHPSheet(Map2D):

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height, False)

    def render(self) -> str:
        return "\n".join(
            "".join("#" if val else "." for val in row)
            for row in self.map
        )

    def fold_horizontal(self, x_value: int) -> None:
        new_width = max(x_value, self.width - 1 - x_value)
        new_map = []
        for row in self.map:
            left_part = row[:x_value]
            right_part = row[x_value + 1:][::-1]
            if len(left_part) > len(right_part):
                right_part = [False] * (len(left_part) - len(right_part)) + right_part
            if len(right_part) > len(left_part):
                left_part = [False] * (len(right_part) - len(left_part)) + left_part
            new_row = [x or y for x, y in zip(left_part, right_part)]
            new_map.append(new_row)
        self.map = new_map

    def fold_vertical(self, y_value: int) -> None:
        new_height = max(y_value, self.height - 1 - y_value)
        new_map = []
        for row_num in range(1, new_height + 1):
            top_row = [False for _ in range(self.width)]
            if (y_value - row_num) >= 0:
                top_row = self.map[y_value - row_num]
            bottom_row = [False for _ in range(self.width)]
            if (y_value + row_num) < self.height:
                bottom_row = self.map[y_value + row_num]
            new_row = [x or y for x, y in zip(top_row, bottom_row)]
            new_map.insert(0, new_row)
        self.map = new_map

    def process_fold(self, fold_line: str) -> None:
        if fold_line.startswith("fold along "):
            fold_line = fold_line[len("fold along "):]
        axes, value = fold_line.split("=")
        return {
            "y": self.fold_vertical,
            "x": self.fold_horizontal
        }[axes](int(value))


if __name__ == "__main__":
    my_input = load_input()
    points, folds = my_input.split("\n\n")
    point_list = points.split("\n")
    coords = [Coords2D.from_input_line(point_line) for point_line in point_list]
    w = max(c.x for c in coords) + 1
    h = max(c.y for c in coords) + 1
    sheet = OHPSheet(w, h)
    for coord in coords:
        sheet.set_value(coord, True)
    print(sheet.render())
    for fold in folds.split("\n"):
        print(fold)
        sheet.process_fold(fold)
        print(sheet.render())
        print(sum(
            row.count(True) for row in sheet.map
        ))
        exit()
    print("Good luck!")
