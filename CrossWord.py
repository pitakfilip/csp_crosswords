from Position import Position


class CrossWord:

    def __init__(self, grid):
        self.grid = grid
        self.ids = 0
        self.intersections = dict()
        self.positions = self.get_positions(grid)

    def get_id(self):
        self.ids += 1
        return self.ids - 1

    def get_positions(self, grid):
        # Computes list of all possible positions for words.
        # Each position is a touple: (start_row, start_col, length, direction),
        # and length must be at least 2, i.e. positions for a single letter
        # (length==1) are omitted.
        # Note: Currently only for 'down' and 'right' directions.
        def check_line(line):
            res = []
            start_i, was_space = 0, False
            for i in range(len(line)):
                if line[i] == '#' and was_space:
                    was_space = False
                    if i - start_i > 1:
                        res.append((start_i, i - start_i))
                elif line[i] == ' ' and not was_space:
                    start_i = i
                    was_space = True
            return res

        poss = []
        for r in range(len(grid)):
            row = grid[r]
            poss = poss + [Position(self.get_id(), r, p[0], p[1], 'right') for p in check_line(row)]
        for c in range(len(grid[0])):
            column = [row[c] for row in grid]
            poss = poss + [Position(self.get_id(), p[0], c, p[1], 'down') for p in check_line(column)]

        p: Position
        for p in poss:
            for pp in poss:
                if p.is_neighbor(pp):
                    p.add_neighbor(pp)
                    if p.d == 'right':
                        self.intersections[p.id, pp.id] = (pp.c - p.c, p.r - pp.r)
                    else:
                        self.intersections[p.id, pp.id] = (pp.r - p.r, p.c - pp.c)
        return poss

    def print_grid(self):
        # Pretty prints the crossword
        for row in self.grid:
            print(''.join(row))

    def text_at_pos(self, position):
        # Returns text actually written in specified position.
        dr, dc = position.dir
        r, c = position.r, position.c
        return ''.join([self.grid[r + i * dr][c + i * dc] for i in range(position.l)])

    def write_word(self, position, word):
        # Writes word to specified position and direction.
        # Note: this method does not check whether the word can be placed into
        # specified position.
        dr, dc = position.dir
        r, c = position.r, position.c
        for i in range(position.l):
            self.grid[r + i * dr][c + i * dc] = word[i]
