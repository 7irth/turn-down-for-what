__author__ = 'tirth'

# Implementation of Conway's Game of life
#
# Works best in command line, cmd or terminal,
# try out the sample starting patterns or add in your own!

from os import system, name
from time import sleep


class Cell:
    def __init__(self, pos=None, alive=False):
        if pos:
            self.x_pos = pos[0]
            self.y_pos = pos[1]

        self.alive = alive
        self.next = False

    def __repr__(self):
        return [' ', '■'][self.alive]  # □


class Grid:
    def __init__(self, x_size=5, y_size=5):
        self.grid = {}
        self.x_size = x_size
        self.y_size = y_size

        # create grid
        for x in range(self.x_size):
            y = ['' for _ in range(self.y_size)]
            self.grid[x] = y
            for y in range(self.y_size):
                self.grid[x][y] = Cell((x, y))

    def __str__(self):
        s = ''

        for y in reversed(range(self.y_size)):
            for x in self.grid.keys():
                s += str(self.grid[x][y]) + ' '
            s += '\n'
        return s

    def update(self, runs=1, delay=0.5, debug=False):
        if debug:
            self.print_grid()
        else:
            for _ in range(runs):
                print(self)
                sleep(delay)
                system('cls' if name == 'nt' else 'clear')

                # figure out next positions
                for x in self.grid.keys():
                    for y in range(self.y_size):
                        c = self.get_cell((x, y))
                        self.life_algo(c)

                # update grid
                for x in self.grid.keys():
                    for y in range(self.y_size):
                        c = self.get_cell((x, y))
                        c.alive = c.next

    def life_algo(self, c):
        n = self.neighbourinos(c)

        if c.alive:
            if n in (2, 3):
                c.next = True
            else:
                c.next = False
        else:
            if n == 3:
                c.next = True

    def print_grid(self):
        for y in reversed(range(self.y_size)):
            if y < 10:
                print(y, end=' | ')
            else:
                print(y, end='| ')
            for x in self.grid.keys():
                if Cell.__repr__(self.grid[x][y]) == ' ':
                    print('□', end=' ')
                else:
                    print(self.grid[x][y], end=' ')
            print()

    def add_cell(self, c):
        self.grid[c.x_pos][c.y_pos] = c

    def get_cell(self, pos):
        return self.grid[pos[0]][pos[1]]

    def turn_on(self, pos):
        c = self.get_cell(pos)
        c.alive = True

    def turn_off(self, pos):
        c = self.get_cell(pos)
        c.alive = False

    def neighbourinos(self, c):
        x = c.x_pos
        y = c.y_pos
        bros = 0

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i, j) != (x, y):
                    try:
                        c = self.get_cell((i, j))
                        if c.alive:
                            bros += 1
                    except KeyError:
                        # print('keys up')
                        pass
                    except IndexError:
                        # print('index up')
                        pass
        return bros

if __name__ == '__main__':
    g = Grid(40, 19)

    # sample starting patterns
    pulsar = [(4, 2), (5, 2), (6, 2), (10, 2), (11, 2), (12, 2),
              (2, 4), (7, 4), (9, 4), (14, 4),
              (2, 5), (7, 5), (9, 5), (14, 5),
              (2, 6), (7, 6), (9, 6), (14, 6),
              (4, 7), (5, 7), (6, 7), (10, 7), (11, 7), (12, 7),
              (4, 9), (5, 9), (6, 9), (10, 9), (11, 9), (12, 9),
              (2, 10), (7, 10), (9, 10), (14, 10),
              (2, 11), (7, 11), (9, 11), (14, 11),
              (2, 12), (7, 12), (9, 12), (14, 12),
              (4, 14), (5, 14), (6, 14), (10, 14), (11, 14), (12, 14)]

    infinite_1 = [(1, 1), (3, 1), (3, 2), (5, 3), (5, 4), (5, 5), (7, 4),
                  (7, 5), (7, 6), (8, 5)]

    infinite_2 = [(1, 1), (3, 1), (5, 1), (2, 2), (3, 2), (5, 2), (4, 3),
                  (5, 3), (1, 4), (1, 5), (2, 5), (3, 5), (5, 5)]

    gun = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
             (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (18, 1), (19, 1),
             (20, 1), (27, 1), (28, 1), (29, 1), (30, 1), (31, 1), (32, 1),
             (33, 1), (35, 1), (36, 1), (37, 1), (38, 1), (39, 1)]

    for cell in gun:  # put starting pattern here
        g.turn_on(cell)

    g.update(169, 0.2)