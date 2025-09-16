import random
import numpy

from tile import Tile

GRID_SIZE = 8

class GameState:
    def __init__(self):
        self.grid = numpy.empty((GRID_SIZE, GRID_SIZE), dtype = object)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.grid[r][c] = Tile(0, False)

        self.bomb_count = 10
        self.randomise_bombs(self.bomb_count)
        self.init_tiles()


    def restart(self):
        self.__init__()


    def randomise_bombs(self, num_bombs: int):
        for i in range(num_bombs):
            while True:
                r = random.randint(0, GRID_SIZE-1)
                c = random.randint(0, GRID_SIZE-1)
                if self.grid[r][c].value != -1:
                    self.grid[r][c].value = -1
                    break

    def init_tiles(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c].value == -1:
                    continue # ignore if bomb

                self.grid[r][c].value = self.count_adjacent_bombs(r,c)

    def count_adjacent_bombs(self, row: int, col: int) -> int:
        count = 0

        for rr in [-1, 0, 1]:
            for cc in [-1, 0, 1]:
                if rr == 0 and cc == 0:
                    continue
                r, c = row + rr, col + cc
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    if self.grid[r][c].value == -1:
                        count += 1

        return count

    def reveal(self, x: int, y: int):
        if self.grid[x][y].visible == True: return

        self.grid[x][y].reveal()

        # if tile = 0 flood reveal all other tiles with 0
        if self.grid[x][y].value == 0:
            neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for xx, yy in neighbors:
                r, c = x + xx, y + yy
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    self.reveal(r, c)
