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


class PacManMaze(Maze):
    def __init__(self, width, height):
        """
        Maze that generates itself to function like a Pac-man maze.

        :param width: width in cells of the maze
        :param height: height in cells of the maze
        """

        super().__init__(width, height)
        self.half_width = self.width // 2
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]
        self.mirrored = ["W", "E", "N", "S"]
        self.looping = False

    def modify_cell(self, x, y, direction):
        """
        Changes both a cell and its mirrored cell.

        :param x: horizontal position of the real cell
        :param y: vertical position of the real cell
        :param direction: wall to carve on the real cell
        """

        cell = self.get_cell_2d(x, y)
        mirror_x = self.width - x - 1
        mirror_cell = self.get_cell_2d(mirror_x, y)
        dir_id = self.directions.index(direction)
        cell.walls.remove(direction)
        mirror_cell.walls.remove(self.mirrored[dir_id])
        self.modified.add(cell)
        self.modified.add(mirror_cell)

    async def carve_hole(self, delay):
        """
        Create a 6x4 hole in the middle of the maze to host the ghosts.

        :param delay: time is seconds to wait for every step
        """

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
        """
        Carve the paths in the maze using the Sidewinder algorithm.

        :param delay:
        :return:
        """

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
        """
        Remove all the dead-ends and the central wall of the maze.

        :param delay: time to wait for in seconds
        """

        for y in range(self.height):
            for x in range(self.half_width):
                cell = self.get_cell_2d(x, y)
                if x == self.half_width - 1 and not cell.visited:
                    self.modify_cell(x, y, "E")
                else:
                    # Having more than two walls means either un-carved or an end.
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
        """
        Generate a Pac-man maze.
        First carve the central hole for the ghosts.
        Second, carve the path with the sidewinder algorithm.
        Lastly, remove all dead-ends as well as the central wall that gets created.
        All the process is mirrored on each halves of the maze to have symmetry.

        :param delay: time in seconds to wait for every step
        """

        await self.carve_hole(delay)
        await self.carve_path(delay)
        await self.loop(delay)
