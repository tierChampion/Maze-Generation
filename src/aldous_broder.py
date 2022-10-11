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
    def __init__(self, width, height):
        super().__init__(width, height)
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]

    def choose_neighbour(self, x, y):
        data = list(zip(self.directions, self.dx, self.dy, self.inverses))
        random.shuffle(data)
        self.directions, self.dx, self.dy, self.inverses = zip(*data)
        for d in range(len(self.directions)):
            new_x = x + self.dx[d]
            new_y = y + self.dy[d]
            if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.width:
                continue
            return new_x, new_y, d

    async def generate(self, delay):
        current_x = random.randint(0, self.width - 1)
        current_y = random.randint(0, self.height - 1)
        current_cell = self.get_cell(current_x, current_y)
        current_cell.visited = True
        remaining = self.width * self.height - 1
        while remaining > 0:
            new_x, new_y, index = self.choose_neighbour(current_x, current_y)
            neighbour_cell = self.get_cell(new_x, new_y)
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
