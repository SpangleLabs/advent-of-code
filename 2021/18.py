import dataclasses
import datetime
from abc import ABC, abstractmethod
from typing import List

from utils.input import load_lines
from utils.types import is_int


@dataclasses.dataclass
class FlattenedValue:
    value: int
    depth: int


@dataclasses.dataclass
class FlattenedNumber:
    value: "Number"
    depth: int


class Number(ABC):

    @abstractmethod
    def max_depth(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def should_split(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def split_result(self) -> "SnailfishNumber":
        raise NotImplementedError

    @abstractmethod
    def flatten(self) -> List[FlattenedValue]:
        raise NotImplementedError

    @abstractmethod
    def magnitude(self) -> int:
        raise NotImplementedError


class RegularNumber(Number):

    def __init__(self, value: int) -> None:
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)

    def max_depth(self) -> int:
        return 0

    def should_split(self) -> bool:
        return self.value >= 10

    def split_result(self) -> "Number":
        left = RegularNumber(self.value // 2)
        right = RegularNumber((self.value + 1) // 2)
        return SnailfishNumber(left, right)

    def flatten(self) -> List[FlattenedValue]:
        return [FlattenedValue(self.value, 0)]

    def magnitude(self) -> int:
        return self.value


class SnailfishNumber(Number):

    def __init__(self, left: Number, right: Number) -> None:
        self.left = left
        self.right = right

    @classmethod
    def parse_input(cls, snailfish_input: str) -> "SnailfishNumber":
        stack = []
        for char in snailfish_input:
            if is_int(char):
                stack.append(RegularNumber(int(char)))
            if char == "]":
                right = stack.pop()
                left = stack.pop()
                number = cls(left, right)
                stack.append(number)
        return stack.pop()

    def reduce(self) -> None:
        while self.should_explode() or self.should_split():
            if self.should_explode():
                self.explode()
                continue
            if self.should_split():
                self.split()
                continue

    def should_explode(self) -> bool:
        return self.max_depth() > 4

    def should_split(self) -> bool:
        return self.left.should_split() or self.right.should_split()

    def explode(self) -> None:
        flatten = self.flatten()
        for i, flat in enumerate(flatten):
            if 4 < flat.depth == flatten[i + 1].depth:
                left = flat
                right = flatten[i + 1]
                if i > 0:
                    flatten[i - 1].value += left.value
                if i + 2 < len(flatten):
                    flatten[i + 2].value += right.value
                flatten = flatten[:i] + [FlattenedValue(0, left.depth - 1)] + flatten[i + 2:]
                break
        stack = [FlattenedNumber(RegularNumber(flat.value), flat.depth) for flat in flatten]
        while len(stack) != 1:
            for i, flat in enumerate(stack):
                if flat.depth == stack[i + 1].depth:
                    left = flat.value
                    right = stack[i + 1].value
                    stack = stack[:i] + [FlattenedNumber(SnailfishNumber(left, right), flat.depth - 1)] + stack[i + 2:]
                    break
        result = stack.pop().value
        assert isinstance(result, SnailfishNumber)
        self.left = result.left
        self.right = result.right

    def split(self) -> None:
        if self.left.should_split():
            self.left = self.left.split_result()
            return
        if self.right.should_split():
            self.right = self.right.split_result()
            return

    def split_result(self) -> "SnailfishNumber":
        if self.left.should_split():
            self.left = self.left.split_result()
            return self
        if self.right.should_split():
            self.right = self.right.split_result()
            return self

    def max_depth(self) -> int:
        return 1 + max(self.left.max_depth(), self.right.max_depth())

    def flatten(self) -> List[FlattenedValue]:
        flatten = self.left.flatten() + self.right.flatten()
        return [FlattenedValue(flat.value, flat.depth + 1) for flat in flatten]

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def __repr__(self):
        return f"[{self.left},{self.right}]"

    def __add__(self, other: "SnailfishNumber") -> "SnailfishNumber":
        new_number = SnailfishNumber(self, other)
        new_number.reduce()
        return new_number


def _main() -> str:
    my_input = load_lines()
    numbers = [SnailfishNumber.parse_input(line) for line in my_input]
    result = numbers[0]
    for number in numbers[1:]:
        result += number
        print(result)
    return str(result.magnitude())


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(_main())
    print(f"Time taken: {(datetime.datetime.now() - start_time).total_seconds()}s")
