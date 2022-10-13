from src.maze import Cell, Maze
import pygame
import random
import asyncio

vec = pygame.math.Vector2

'''
By definition, a Pac-man maze must be horizontally symmetric, and must not have dead ends.
To make such a maze, you first generate a half maze on it's left side only and with a hole in the middle of the right 
side, remove random walls on the cells such that every cell has two or less walls, which removes dead-ends, and then
you simply mirror this maze while removing the inner most wall. In this implementation, the actual maze generation is 
that of the Sidewinder, but on its side, such that you also get a long path along the sides of the maze.
'''

# TODO Remove as many cells to render as possible with the positive version (render row by row kind of)


def negative_draw(win, dimension, cell):
    top_left = vec((cell.col + 1) * dimension, (cell.row + 1) * dimension)
    top_right = top_left + vec(dimension, 0)
    bottom_left = top_left + vec(0, dimension)
    bottom_right = top_left + vec(dimension, dimension)

    pygame.draw.rect(win, (0, 0, 0), [top_left, vec(dimension, dimension)], 2)

    if "N" in cell.walls:
        pygame.draw.line(win, (255, 255, 255), top_left, top_right, 1)
    if "S" in cell.walls:
        pygame.draw.line(win, (255, 255, 255), bottom_left, bottom_right, 1)
    if "E" in cell.walls:
        pygame.draw.line(win, (255, 255, 255), top_right, bottom_right, 1)
    if "W" in cell.walls:
        pygame.draw.line(win, (255, 255, 255), top_left, bottom_left, 1)


class PacManMaze(Maze):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.half_width = self.width // 2
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]
        self.mirrored = ["W", "E", "N", "S"]
        self.looping = False

    def modify_cell(self, x, y, direction):
        cell = self.get_cell_2d(x, y)
        mirror_x = self.width - x - 1
        mirror_cell = self.get_cell_2d(mirror_x, y)
        dir_id = self.directions.index(direction)
        cell.walls.remove(direction)
        mirror_cell.walls.remove(self.mirrored[dir_id])
        self.modified.add(cell)
        self.modified.add(mirror_cell)

    async def carve_hole(self, delay):
        y_min = self.height // 2
        y_max = self.height // 2 + 3
        x_min = self.half_width - 3
        x_max = self.half_width
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                cell = self.get_cell_2d(x, y)
                cell.visited = True
                self.modify_cell(x, y, "E")
                if x > x_min:
                    self.modify_cell(x, y, "W")
                if y != y_max - 1:
                    self.modify_cell(x, y, "S")
                if y != y_min:
                    self.modify_cell(x, y, "N")
                await asyncio.sleep(delay)

    async def carve_path(self, delay):
        for x in range(self.half_width):
            run = []
            for y in range(self.height):
                cell = self.get_cell_2d(x, y)
                if cell.visited:
                    continue
                run.append(cell)
                if y == 0 and x == 0:
                    continue
                elif x == 0:
                    move = 1
                elif y - 1 < 0 or self.get_cell_2d(x, y - 1).visited:
                    move = 0
                else:
                    move = random.randint(0, 1)
                if move == 1:
                    self.modify_cell(x, y, "N")
                    self.modify_cell(x, y - 1, "S")
                elif move == 0:
                    selected_cell = run[random.randint(0, len(run) - 1)]
                    self.modify_cell(selected_cell.col, selected_cell.row, "W")
                    self.modify_cell(x - 1, selected_cell.row, "E")
                    run.clear()
                await asyncio.sleep(delay)

    async def loop(self, delay):
        for y in range(self.height):
            for x in range(self.half_width):
                cell = self.get_cell_2d(x, y)
                if x == self.half_width - 1 and not cell.visited:
                    self.modify_cell(x, y, "E")
                else:
                    while len(cell.walls) > 2:
                        next_x = -1
                        next_y = -1
                        i = 0
                        while next_x < 0 or next_y < 0 or next_y >= self.height or \
                                self.get_cell_2d(next_x, next_y).visited:
                            direction = random.choice(cell.walls)
                            i = self.directions.index(direction)
                            next_x = x + self.dx[i]
                            next_y = y + self.dy[i]
                        self.modify_cell(x, y, self.directions[i])
                        self.modify_cell(next_x, next_y, self.inverses[i])
                await asyncio.sleep(delay)

    async def generate(self, delay):
        self.looping = False
        await self.carve_hole(delay)
        await self.carve_path(delay)
        self.looping = True
        await self.loop(delay)

    async def render(self, win: pygame.display, dimension: float, delay: float):
        white = pygame.color.Color((255, 255, 255))
        for i in range(self.width * self.height):

            for cell in self.modified:
                negative_draw(win, dimension, cell)

            self.modified.clear()

            pygame.draw.rect(win, white,
                             [dimension, dimension, dimension * self.width + 2, dimension * self.height + 2], 2)

            pygame.display.update()
            await asyncio.sleep(delay)
