from src.maze import Maze
import pygame
import random
import asyncio

vec = pygame.math.Vector2

'''
Generates a minimum spanning tree maze. Starts at a random vertex and goes to a random neighbour,
which becomes the current vertex. It is very slow as a maze generation algorithm.
'''


class AldousBroderMaze(Maze):
    def __init__(self, width: int, height: int):
        """
        Maze that generates itself using the Aldous-Broder Algorithm

        :param width: Width in cells of the maze
        :param height: Height in cells of the maze
        """

        super().__init__(width, height)
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]

    def choose_neighbour(self, x: int, y: int):
        """
        Find a random valid neighbour of the current cell.

        :param x: Lateral position of the current cell
        :param y: Vertical position of the current cell
        :return: Position of the neighbour and the move to get to it.
        """

        # Shuffle the different move possibilities
        data = list(zip(self.directions, self.dx, self.dy, self.inverses))
        random.shuffle(data)
        self.directions, self.dx, self.dy, self.inverses = zip(*data)

        # Return the position of the first neighbour encountered
        for d in range(len(self.directions)):
            new_x = x + self.dx[d]
            new_y = y + self.dy[d]
            if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.width:
                continue
            return new_x, new_y, d

    async def generate(self, delay: float):
        """
        Generate a maze with the Aldous-Broder Algorithm.
        Choose a starting cell and gradually go to it's neighbouring cells, carving a path if the cell wasn't visited.
        The algorithm wastes a lot of time not carving paths but it generates minimum spanning trees and has an
        equal probability to generate any maze.

        :param delay: time in seconds to wait for every step.

        """

        # Pick the starting cell
        current_x = random.randint(0, self.width - 1)
        current_y = random.randint(0, self.height - 1)
        current_cell = self.get_cell_2d(current_x, current_y)
        current_cell.visited = True
        remaining = self.width * self.height - 1
        while remaining > 0:
            # Find a neighbour and carve to it if it wasn't already carved to.
            new_x, new_y, index = self.choose_neighbour(current_x, current_y)
            neighbour_cell = self.get_cell_2d(new_x, new_y)
            if not neighbour_cell.visited:
                await asyncio.sleep(delay)
                remaining -= 1
                neighbour_cell.visited = True
                current_cell.walls.remove(self.directions[index])
                neighbour_cell.walls.remove(self.inverses[index])
                self.modified.add(current_cell)
                self.modified.add(neighbour_cell)
            current_x = new_x
            current_y = new_y
            current_cell = neighbour_cell
