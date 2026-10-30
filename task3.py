import random


class SnakeMatrix:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            data = args[0]

            if not data or not isinstance(data[0], list):
                raise ValueError("Матрица не должна быть пустой.")
            
            self._rows = len(data)
            self._cols = len(data[0])
            
            if self._rows == 0 or self._cols == 0:
                raise ValueError("Количество строк и столбцов должно быть больше нуля.")
                
            if not all(isinstance(row, list) and len(row) == self._cols for row in data):
                raise ValueError("Все строки матрицы должны иметь одинаковую длину.")
                
            self._matrix = [row[:] for row in data]
            
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            rows, cols = args[0], args[1]
            if rows <= 0 or cols <= 0:
                raise ValueError("Количество строк и столбцов должно быть больше нуля.")
                
            self._rows = rows
            self._cols = cols
            self._matrix = [[random.randint(1, 9999) for _ in range(cols)] for _ in range(rows)]
            
        else:
            raise ValueError("Некорректные аргументы конструктора.")

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def __len__(self):
        return self._rows * self._cols

    def __getitem__(self, key):
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("Индексы должны быть переданы в формате (row, col).")

        row, col = key
        if not (0 <= row < self._rows) or not (0 <= col < self._cols):
            raise IndexError("Индекс вышел за пределы матрицы.")
            
        return self._matrix[row][col]

    def __contains__(self, item):
        return any(item in row for row in self._matrix)

    def __iter__(self):
        return SnakeMatrixIterator(self)

    def __str__(self):
        return "\n".join(" ".join(f"{elem:4d}" for elem in row) for row in self._matrix)


class SnakeMatrixIterator:
    def __init__(self, snake_matrix):
        self._matrix = snake_matrix
        self._current_row = 0
        self._current_col = 0

    def __next__(self):
        if self._current_row >= self._matrix.rows:
            raise StopIteration

        element = self._matrix[self._current_row, self._current_col]

        if self._current_row % 2 == 0:
            if self._current_col < self._matrix.cols - 1:
                self._current_col += 1
            else:
                self._current_row += 1
        else:
            if self._current_col > 0:
                self._current_col -= 1
            else:
                self._current_row += 1

        return element


data = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
matrix = SnakeMatrix(data)

print("Матрица:")
print(matrix)
print(f"Количество элементов: {len(matrix)}")
print(f"Элемент: {matrix[1, 2]}")
print(f"Есть ли 5 в матрице? {5 in matrix}")

print("\nОбход змейкой:")
iterator = iter(matrix)
for value in matrix:
    print(value, end=" ")


random_matrix = SnakeMatrix(4, 4)
print("Случайная матрица:")
print(random_matrix)
print("Обход случайной матрицы:")
print(list(random_matrix))