
# Represents a unit on the crossword grid, where we want to write a word
# The position's neighbor is another position intersecting it
class Position:
    def __init__(self, id, row, column, length, direction):
        self.id = id
        self.r = row
        self.c = column
        self.l = length
        self.d = direction
        self.dir = {'down': (1, 0), 'right': (0, 1)}[direction]
        self.neighbors = set()

    def __str__(self):
        return '[#{}, r:{}, c:{}, l:{}, dir:{}]'.format(self.id, self.r, self.c, self.l, self.d)

    def __repr__(self):
        return '<' + self.__str__() + '>'

    def add_neighbor(self, p):
        self.neighbors.add(p)

    # Calculate whether another position intersects this point
    def is_neighbor(self, p):
        if self.d == p.d:
            return False

        if (self.d == 'down'):
            return self.r <= p.r < (self.r + self.l) and p.c <= self.c <= (p.c + p.l)

        return self.c <= p.c < (self.c + self.l) and p.r <= self.r <= (p.r + p.l)
