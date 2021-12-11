from typing import List, TypeVar, Tuple, Union, Generic, Iterator, Callable

S = TypeVar("S")
T = TypeVar("T")


class Grid(Generic[T]):
    def __init__(self, arr: List[List[T]]) -> None:
        self.arr = arr

    @property
    def height(self) -> int:
        return len(self.arr)

    @property
    def width(self) -> int:
        return len(self.arr[0])

    def __contains__(self, yx: Tuple[int, int]) -> bool:
        y, x = yx
        return 0 <= y < self.height and 0 <= x < self.width

    def __getitem__(self, yx: Union[Tuple[int, int], int]) -> Union[T, List[T]]:
        if isinstance(yx, tuple):
            if yx not in self:
                raise IndexError
            y, x = yx
            return self.arr[y][x]
        elif not isinstance(yx, int):
            raise TypeError
        return self.arr[yx]

    def __iter__(self) -> Iterator[T]:
        return self.row_major()

    def row_major_with_index(self) -> Iterator[Tuple[Tuple[int, int], T]]:
        for i in range(self.height):
            for j in range(self.width):
                yield ((i, j), self.arr[i][j])

    def row_major(self) -> Iterator[T]:
        for ((_, _), elem) in self.row_major_with_index():
            yield elem

    def column_major_with_index(self) -> Iterator[Tuple[Tuple[int, int], T]]:
        for i in range(self.width):
            for j in range(self.height):
                yield ((i, j), self.arr[j][i])

    def column_major(self) -> Iterator[T]:
        for ((_, _), elem) in self.column_major_with_index():
            yield elem

    def apply(self, func: Callable[[T], None]) -> None:
        for item in self:
            func(item)

    def map(self, func: Callable[[T], S]) -> "Grid[S]":
        return Grid([[func(item) for item in row] for row in self.arr])

    def around_with_index(
        self, yx: Tuple[int, int]
    ) -> Iterator[Tuple[Tuple[int, int], T]]:
        y, x = yx
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (y + i, x + j) in self:
                    yield ((y + i, x + j), self.arr[y + i][x + j])

    def around(self, yx: Tuple[int, int]) -> Iterator[T]:
        for ((_, _), elem) in self.around_with_index(yx):
            yield elem
