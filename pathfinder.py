import pygame
import queue
from queue import PriorityQueue
from spot import Spot
from pygame.locals import *
import mazes

pygame.init()


RED = (255, 0, 0)
DARKRED = (180, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 180, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
LIGHTGREY = (150, 150, 150)
TURQUOISE = (64, 224, 208)

SIZE = 600
RIGHT_SPACE = 200
WIN = pygame.display.set_mode((SIZE + RIGHT_SPACE, SIZE))
pygame.display.set_caption('PathFinder')

button_font = pygame.font.SysFont('Constantia', 20)
record_font = pygame.font.SysFont('Areal', 15)

class Button:
    def __init__(self, x, y, width, height, color, color_hover, color_selected, label, selected = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.color_hover = color_hover
        self.color_selected = color_selected
        self.label = label
        self.selected = selected


    def draw_button(self, win):
        pos = pygame.mouse.get_pos()
        button_space = Rect(self.x, self.y, self.width, self.height)

        if button_space.collidepoint(pos) and not self.selected:
            pygame.draw.rect(win, self.color_hover, button_space)
        else:
            pygame.draw.rect(win, self.color, button_space)
        if self.selected:
            pygame.draw.rect(win, self.color_selected, button_space)

        text = button_font.render(self.label, True, BLACK)
        text_length = text.get_width()
        text_height = text.get_height()
        win.blit(text, (self.x + int(self.width / 2) - int(text_length / 2), self.y + int(self.height / 2) - int(text_height / 2)))


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    length = 0
    while current in came_from:
        current = came_from[current]
        current.make_path()
        length += 1
        draw()
    return length

def print_record(win, path, steps):
    win.blit(record_font.render('Steps: f{steps}', True, BLACK), (620, 240))
    win.blit(record_font.render('Path: f{path}', True, BLACK), (620, 240))


def a_star(draw, grid, start, end):
    count = 0
    steps = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf')for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            length = reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            print(f"Steps: {steps}")
            print(f"Path length: {length}")
            return True

        steps += 1
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def BFS(draw, start, end):
    open_set = queue.Queue()
    visited = set()
    came_from = {}
    steps = 0
    open_set.put(start)
    visited.add(start)

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()

        if current == end:
            length = reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            #print_record(WIN, length, steps)
            print(f"Steps: {steps}")
            print(f"Path length: {length}")
            return True

        steps += 1
        for neighbor in current.neighbors:
            if neighbor.is_blank() or neighbor.is_end() and neighbor not in visited:
                came_from[neighbor] = current
                open_set.put(neighbor)
                visited.add(current)
                neighbor.make_open()

        if current != start:
            current.make_closed()
        draw()
    return False


def DFS(draw, start, end):
    visited = set()
    came_from = {}
    steps = 0
    s = [start]

    while s:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = s[-1]
        visited.add(current)

        if current == end:
            length = reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            print(f"Steps: {steps}")
            print(f"Path length: {length}")
            return True
        steps += 1

        for neighbor in current.neighbors:
            if neighbor.is_blank() or neighbor.is_end() and neighbor not in visited:
                came_from[neighbor] = current
                s.append(neighbor)

        if s[-1] == current:
            s.pop()

        if current != start:
            current.make_closed()
        draw()
    return False


def make_grid(rows, size):
    grid = []
    gap = size // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, size):
    gap = size // rows
    for i in range(rows+1):
        pygame.draw.line(win, GREY, (0, i * gap), (size, i * gap))
        for j in range(rows+1):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, size))


def draw(win, grid, rows, size, buttons):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    for button in buttons:
        buttons[button].draw_button(win)
    draw_grid(win, rows, size)
    pygame.display.update()


def get_clicked_pos(pos, rows, size):
    gap = size // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def create_buttons():
    buttons = {}
    buttons['astar'] = Button(620, 30, 160, 50, GREY, LIGHTGREY, ORANGE, 'A* PathFinder')
    buttons['BFS'] = Button(620, 90, 160, 50, GREY, LIGHTGREY, ORANGE, 'BFS PathFinder')
    buttons['DFS'] = Button(620, 150, 160, 50, GREY, LIGHTGREY, ORANGE, 'DFS PathFinder')
    buttons['start'] = Button(620, 520, 75, 50, DARKGREEN, GREEN, ORANGE, 'START')
    buttons['reset'] = Button(705, 520, 75, 50, DARKRED, RED, ORANGE, 'RESET')
    buttons['maze1'] = Button(620, 320, 160, 50, GREY, LIGHTGREY, ORANGE, 'I')
    buttons['maze2'] = Button(620, 380, 160, 50, GREY, LIGHTGREY, ORANGE, 'II')
    buttons['maze3'] = Button(620, 440, 160, 50, GREY, LIGHTGREY, ORANGE, 'III')
    return buttons


def create_maze(grid, maze):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if maze[i][j] == "#":
                grid[i][j].color = BLACK



def main(win, size):
    ROWS = 50
    grid = make_grid(ROWS, size)
    buttons = create_buttons()
    start = None
    end = None
    run= True
    while run:
        draw(win, grid, ROWS, size, buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] < size and pos[1] < size:
                    row, col = get_clicked_pos(pos, ROWS, size)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

                elif pos[0] > buttons['astar'].x \
                    and pos[0] < (buttons['astar'].x + buttons['astar'].width) \
                    and pos[1] > buttons['astar'].y\
                    and pos[1] < (buttons['astar'].y + buttons['astar'].height):
                    buttons['astar'].selected = True
                    buttons['BFS'].selected = False
                    buttons['DFS'].selected = False

                elif pos[0] > buttons['BFS'].x \
                    and pos[0] < (buttons['BFS'].x + buttons['BFS'].width) \
                    and pos[1] > buttons['BFS'].y\
                    and pos[1] < (buttons['BFS'].y + buttons['BFS'].height):
                    buttons['astar'].selected = False
                    buttons['BFS'].selected = True
                    buttons['DFS'].selected = False

                elif pos[0] > buttons['DFS'].x \
                    and pos[0] < (buttons['DFS'].x + buttons['DFS'].width) \
                    and pos[1] > buttons['DFS'].y\
                    and pos[1] < (buttons['DFS'].y + buttons['DFS'].height):
                    buttons['astar'].selected = False
                    buttons['BFS'].selected = False
                    buttons['DFS'].selected = True

                elif pos[0] > buttons['maze1'].x \
                    and pos[0] < (buttons['maze1'].x + buttons['maze1'].width) \
                    and pos[1] > buttons['maze1'].y \
                    and pos[1] < (buttons['maze1'].y + buttons['maze1'].height):
                    create_maze(grid, maze1)

                elif pos[0] > buttons['maze2'].x \
                    and pos[0] < (buttons['maze2'].x + buttons['maze2'].width) \
                    and pos[1] > buttons['maze2'].y \
                    and pos[1] < (buttons['maze2'].y + buttons['maze2'].height):
                    pass

                elif pos[0] > buttons['maze3'].x \
                    and pos[0] < (buttons['maze3'].x + buttons['maze3'].width) \
                    and pos[1] > buttons['maze3'].y \
                    and pos[1] < (buttons['maze3'].y + buttons['maze3'].height):
                    pass

                elif start and end \
                    and pos[0] > buttons['start'].x \
                    and pos[0] < (buttons['start'].x + buttons['start'].width) \
                    and pos[1] > buttons['start'].y\
                    and pos[1] < (buttons['start'].y + buttons['start'].height):
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    if buttons['astar'].selected:
                        a_star(lambda: draw(win, grid, ROWS, size, buttons), grid, start, end)
                    if buttons['BFS'].selected:
                        BFS(lambda: draw(win, grid, ROWS, size, buttons), start, end)
                    if buttons['DFS'].selected:
                        DFS(lambda: draw(win, grid, ROWS, size, buttons), start, end)

                elif pos[0] > buttons['reset'].x \
                    and pos[0] < (buttons['reset'].x + buttons['reset'].width) \
                    and pos[1] > buttons['reset'].y \
                    and pos[1] < (buttons['reset'].y + buttons['reset'].height):
                    start = None
                    end = None
                    grid = make_grid(ROWS, size)


            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if pos[0] < size and pos[1] < size:
                    row, col = get_clicked_pos(pos, ROWS, size)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

    pygame.quit()

main(WIN, SIZE)
