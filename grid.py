class Grid:
    def __init__(self, rows = 20,cols = 20, survive=[2,3], new = [3]):
        self.rows = rows
        self.cols = cols
        self.cells = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.survive = survive
        self.new = new

    def toggle_cell(self,row,col):
        if 0 <= row < self.rows and  0 <= col < self.cols:
            self.cells[row][col] = 1 - self.cells[row][col] # Будет либо 1 - 0 = 1 или 1 - 1 = 0

    def count_neighbors(self,row,col):
        count = 0
        for y in range(row-1,row+2):
            for x in range(col-1,col+2):
                if (0 <= y < self.rows) and (0 <= x < self.cols):
                    if (y, x) != (row, col):
                        count += self.cells[y][x]
        return count

    def next_generation(self):
        new_cells = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.cols):
                neighbors = self.count_neighbors(y,x)
                if self.cells[y][x] == 1:
                    if neighbors in self.survive:
                        new_cells[y][x] = 1
                else:
                    if neighbors in self.new:
                        new_cells[y][x] = 1
        self.cells = new_cells

    def set_rules(self, survive = None, new = None):
        if survive is not None:
            self.survive = survive
        if new is not None:
            self.new = new