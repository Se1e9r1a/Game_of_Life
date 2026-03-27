class Grid:
    def __init__(self):
        self.alive = set()
        self.birth_rules = [3]
        self.survive_rules = [2, 3]

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

            for row, col in self.alive:
                candidates.add((row, col))
                for y in range(row - 1, row + 2):
                    for x in range(col - 1, col + 2):
                        candidates.add((y, x))

            for cell in candidates:
                r, c = cell 
                count = self.count_neighbors(r, c)
                
                if cell in self.alive:
                    if count in self.survive_rules:
                        new_alive.add(cell)
                else:
                    if count in self.birth_rules:
                        new_alive.add(cell)
            
            self.alive = new_alive

    def set_rules(self, survive=None, birth=None):
        if survive is not None:
            self.survive = survive
        if birth is not None:
            self.birth = birth

    def insert_pattern(self, pattern_name: str, top_left: tuple[int, int]):
        from patterns import PATTERNS
        if pattern_name not in PATTERNS:
            return

        row_offset, col_offset = top_left
        for r, c in PATTERNS[pattern_name]:
            self.alive.add((r + row_offset, c + col_offset))