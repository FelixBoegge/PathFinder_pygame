import pygame


WHITE = (255, 255, 255)     # blank spot
BLACK = (0, 0, 0)           # barrier

ORANGE = (255, 165, 0)      # start
TURQUOISE = (64, 224, 208)  # end
PURPLE = (128, 0, 128)      # path

GREEN = (0, 255, 0)         # open spot
RED = (255, 0, 0)           # closed spot


class Spot:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_blank(self):
        return self.color == WHITE

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_path(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw_full(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def draw_path(self, win):
        pygame.draw.circle(win, self.color, (self.x + self.size/2, self.y + self.size/2), (self.size/2)*.8)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():                  # Left
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():# Right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():                  # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():# Down
            self.neighbors.append(grid[self.row + 1][self.col])


   # def __lt__(self, other):
   #     return False
