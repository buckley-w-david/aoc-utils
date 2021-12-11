class Grid:
    def __init__(self, arr):
        self.arr = arr
        self.height = len(arr)
        self.width = len(arr[0])

    def __contains__(self, yx):
        y, x = yx
        return 0 <= y < self.height and 0 <= x < self.width

    def __getitem__(self, yx):
        if isinstance(yx, Tuple):
            if yx not in self:
                raise IndexError
            y, x = yx
            return self.arr[y][x]
        elif not isinstance(yx, int): 
            raise TypeError
        return self.arr[yx]


    def __iter__(self):
        return iter(self.arr)

    def row_major_with_index(self):
        for i in range(self.height):
            for j in range(self.width):
                yield ((i, j), self.arr[i][j])

    def row_major(self):
        for ((_, _), elem) in self.row_major_with_index():
            yield elem

    def column_major_with_index(self):
        for i in range(self.width):
            for j in range(self.height):
                yield ((i, j), self.arr[j][i])

    def column_major(self):
        for ((_, _), elem) in self.column_major_with_index():
            yield elem

    def apply(self, func):
        for row in self:
            for item in row:
                func(item)

    def around_with_index(self, y, x):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (y+i, x+j) in self:
                    yield ((y+i, x+j), self.arr[y+i][x+j])

    def around(self, y, x):
        for ((_, _), elem) in self.around_with_index(y, x):
            yield elem
