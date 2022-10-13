import pygame
import asyncio

vec = pygame.math.Vector2


class Cell:
    def __init__(self, x, y):
        self.col = x
        self.row = y
        self.walls = ["E", "W", "N", "S"]
        self.visited = False


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.empty_grid()
        self.modified = set()

    def empty_grid(self):
        grid = []
        for y in range(self.height):
            for x in range(self.width):
                cell = Cell(x, y)
                grid.append(cell)
        return grid

    def get_cell_2d(self, x, y):
        return self.grid[y * self.width + x]

    def get_cell_1d(self, pos):
        return self.grid[pos]

    def init_render(self, win: pygame.display, dimension: float):
        white = pygame.color.Color((255, 255, 255))
        win.fill(0)
        pygame.draw.rect(win, white,
                         [dimension, dimension, dimension * self.width + 2, dimension * self.height + 2], 2)
        for cell in self.grid:
            top_left = vec((cell.col + 1) * dimension, (cell.row + 1) * dimension)
            top_right = top_left + vec(dimension, 0)
            bottom_left = top_left + vec(0, dimension)
            bottom_right = top_left + vec(dimension, dimension)
            if "N" in cell.walls:
                pygame.draw.aaline(win, white, top_left, top_right)
            if "S" in cell.walls:
                pygame.draw.aaline(win, white, bottom_left, bottom_right)
            if "E" in cell.walls:
                pygame.draw.aaline(win, white, top_right, bottom_right)
            if "W" in cell.walls:
                pygame.draw.aaline(win, white, top_left, bottom_left)
        pygame.display.update()

    async def render(self, win: pygame.display, dimension: float, delay: float):
        black = pygame.color.Color((0, 0, 0))
        white = pygame.color.Color((255, 255, 255))
        for i in range(self.width * self.height):

            for cell in self.modified:
                offset = 1
                size = 2
                if "N" not in cell.walls:
                    start_pos = ((cell.col + 1) * dimension + offset, (cell.row + 1) * dimension)
                    end_pos = ((cell.col + 2) * dimension - offset, (cell.row + 1) * dimension)
                    pygame.draw.line(win, black, start_pos, end_pos, size)
                if "S" not in cell.walls:
                    start_pos = ((cell.col + 1) * dimension + offset, (cell.row + 2) * dimension)
                    end_pos = ((cell.col + 2) * dimension - offset, (cell.row + 2) * dimension)
                    pygame.draw.line(win, black, start_pos, end_pos, size)
                if "E" not in cell.walls:
                    start_pos = ((cell.col + 2) * dimension, (cell.row + 1) * dimension + offset)
                    end_pos = ((cell.col + 2) * dimension, (cell.row + 2) * dimension - offset)
                    pygame.draw.line(win, black, start_pos, end_pos, size)
                if "W" not in cell.walls:
                    start_pos = ((cell.col + 1) * dimension, (cell.row + 1) * dimension + offset)
                    end_pos = ((cell.col + 1) * dimension, (cell.row + 2) * dimension - offset)
                    pygame.draw.line(win, black, start_pos, end_pos, size)
            self.modified.clear()

            pygame.draw.rect(win, white,
                             [dimension, dimension, dimension * self.width + 2, dimension * self.height + 2], 2)

            pygame.display.update()
            await asyncio.sleep(delay)
