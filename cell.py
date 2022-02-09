from pprint import pprint


class Cell:
    def __init__(self, val, x, y, w, h) -> None:
        self.val = val
        self.next_val = val
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.neighbours = []

    def get_neighbor(self, x: int, y: int, grid: list):
        if x < 0:
            x = self.w - 1
        if x > self.w - 1:
            x = 0

        if y < 0:
            y = self.h - 1
        if y > self.h - 1:
            y = 0

        return grid[y][x]

    def find_neighbours(self, grid: list):
        x, y = self.x, self.y
        self.neighbours = [
            self.get_neighbor(x - 1, y - 1, grid),  # 1
            self.get_neighbor(x, y - 1, grid),  # 2
            self.get_neighbor(x + 1, y - 1, grid),  # 3
            self.get_neighbor(x + 1, y, grid),  # 4
            self.get_neighbor(x + 1, y + 1, grid),  # 5
            self.get_neighbor(x, y + 1, grid),  # 6
            self.get_neighbor(x - 1, y + 1, grid),  # 7
            self.get_neighbor(x - 1, y, grid)  # 8
        ]

    def count_live_neighbors(self) -> int:
        count = 0
        for cell in self.neighbours:
            if cell.val == 1:
                count += 1
        return count

    def __str__(self) -> str:
        return f"{self.val}=({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"{self.val}=({self.x}, {self.y})"


if __name__ == '__main__':
    # Use __str__
    print(Cell(0, 1, 2, 100, 100))

    # Use __repr__
    data = [Cell(0, 1, 2, 100, 100)]
    pprint(data)
