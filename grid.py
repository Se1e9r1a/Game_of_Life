class Grid:
    def __init__(self, survive=[2,3], birth=[3]):
        self.alive = set() # множество координат живых клеток

        self.survive = survive
        self.birth = birth

    def toggle_cell(self, row, col):
        cell = (row, col)

        if cell in self.alive:
            self.alive.remove(cell)
        else:
            self.alive.add(cell)

    def count_neighbors(self, row, col):
        count = 0

        for y in range(row - 1, row + 2):
            for x in range(col - 1, col + 2):
                if (y, x) in self.alive and (y, x) != (row, col):
                    count += 1

        return count

    def next_generation(self):
        new_alive = set()
        candidates = set()

        # берём всех живых клеток и их соседей
        for (row, col) in self.alive:
            for y in range(row - 1, row + 2):
                for x in range(col - 1, col + 2):
                    candidates.add((y, x))

        # проверяем только кандидатов
        for (row, col) in candidates:
            neighbors = self.count_neighbors(row, col)

            if (row, col) in self.alive:
                if neighbors in self.survive:
                    new_alive.add((row, col))
            else:
                if neighbors in self.birth:
                    new_alive.add((row, col))

        self.alive = new_alive

    def set_rules(self, survive=None, birth=None):
        if survive is not None:
            self.survive = survive
        if birth is not None:
            self.birth = birth

    # grid.py (внутри класса Grid)

    def insert_pattern(self, pattern_name: str, top_left: tuple[int, int]):
        from patterns import PATTERNS
        if pattern_name not in PATTERNS:
            return

        row_offset, col_offset = top_left
        for r, c in PATTERNS[pattern_name]:
            self.alive.add((r + row_offset, c + col_offset))