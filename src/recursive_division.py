from src.maze import Cell, Maze
import pygame
import random
import asyncio

vec = pygame.math.Vector2

'''
Unlike the other algorithms, int his algorithm you create the walls instead of carving a path.
You first if you want an horizontal or vertical wall. You then randomly determine where it will go,
as well as where the single hole in the wall will go. Recursively do this operation with the two knew halves
created by cutting the initial rectangle with the wall. When the height or width of that rectangle is equal
or smaller then one, you stop. This algorithm creates very square looking maze with a lot of small paths.
'''


class DivisionCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.walls = []


class RecursiveDivisionMaze(Maze):
    def __init__(self, width, height):
        super().__init__(width, height)

    def empty_grid(self):
        grid = []
        for y in range(self.height):
            for x in range(self.width):
                cell = DivisionCell(x, y)
                grid.append(cell)
        return grid

    @staticmethod
    def choose_orientation(width, height):
        horizontal = (width < height)
        if width == height:
            horizontal = random.randint(0, 1) == 0
        return horizontal

    async def recursive_subdivide(self, x, y, width, height, delay):
        if width <= 1 or height <= 1:
            return
        horizontal = self.choose_orientation(width, height)
        await asyncio.sleep(delay)
        if horizontal:
            if height <= 2:
                wall_y = y
            else:
                wall_y = y + random.randrange(0, height - 1, 1)
            opening_x = x + random.randrange(0, width, 1)
            for i in range(width):

                if x + i != opening_x:
                    self.get_cell_2d(x + i, wall_y).walls.append("S")
                    self.modified.add(self.get_cell_2d(x + i, wall_y))
            height1 = wall_y - y + 1
            if height <= 2:
                height1 -= 1
            height2 = height - height1
            if height1 == 0:
                height2 *= 0
            y2 = wall_y + 1
            await self.recursive_subdivide(x, y, width, height1, delay)
            await self.recursive_subdivide(x, y2, width, height2, delay)

        if not horizontal:
            if width <= 2:
                wall_x = x
            else:
                wall_x = x + random.randrange(0, width - 1, 1)
            opening_y = y + random.randrange(0, height, 1)
            for i in range(height):
                if y + i != opening_y:
                    self.get_cell_2d(wall_x, y + i).walls.append("E")
                    self.modified.add(self.get_cell_2d(wall_x, y + i))
            width1 = wall_x - x + 1
            if width <= 2:
                width1 -= 1
            width2 = width - width1
            if width1 == 0:
                width2 *= 0
            x2 = wall_x + 1
            await self.recursive_subdivide(x, y, width1, height, delay)
            await self.recursive_subdivide(x2, y, width2, height, delay)

    async def generate(self, delay):
        await self.recursive_subdivide(0, 0, self.width, self.height, delay)

    async def partial_render(self, win: pygame.display, dimension: float, delay: float):
        white = pygame.color.Color((255, 255, 255))
        for i in range(self.width * self.height):
            for cell in self.grid:
                top_left = vec((cell.col + 1) * dimension, (cell.row + 1) * dimension)
                top_right = top_left + vec(dimension, 0)
                bottom_left = top_left + vec(0, dimension)
                bottom_right = top_left + vec(dimension, dimension)
                if "N" in cell.walls:
                    pygame.draw.line(win, white, top_left, top_right, 1)
                if "S" in cell.walls:
                    pygame.draw.line(win, white, bottom_left, bottom_right, 1)
                if "E" in cell.walls:
                    pygame.draw.line(win, white, top_right, bottom_right, 1)
                if "W" in cell.walls:
                    pygame.draw.line(win, white, top_left, bottom_left, 1)
            pygame.display.update()
            self.modified.clear()
            await asyncio.sleep(delay)
