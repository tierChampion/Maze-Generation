from src.maze import Maze
import pygame
import random
import asyncio

vec = pygame.math.Vector2

'''
Start at known vertex and randomly move to one available neighbour, if there is one. Then,
recursively call this operation. Naturally, if it goes too far and there aren't any neighbours,
it backs up and fills in the gaps. This algorithm tends to create very few and long passages.
'''


class RecursiveBackTrackerMaze(Maze):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]

    async def recursive_track(self, x, y, delay):
        await asyncio.sleep(delay)
        if not self.get_cell_2d(x, y).visited:
            self.get_cell_2d(x, y).visited = True
        data = list(zip(self.directions, self.dx, self.dy, self.inverses))
        random.shuffle(data)
        self.directions, self.dx, self.dy, self.inverses = zip(*data)
        for idx, direction in enumerate(self.directions):
            new_x = x + self.dx[idx]
            new_y = y + self.dy[idx]
            if not (new_x < 0 or new_x > self.width - 1 or new_y < 0 or new_y > self.height - 1):
                if not self.get_cell_2d(new_x, new_y).visited:
                    self.get_cell_2d(new_x, new_y).visited = True
                    self.get_cell_2d(x, y).walls.remove(self.directions[idx])
                    self.get_cell_2d(new_x, new_y).walls.remove(self.inverses[idx])
                    self.modified.add(self.get_cell_2d(x, y))
                    self.modified.add(self.get_cell_2d(new_x, new_y))
                    await self.recursive_track(new_x, new_y, delay)

    async def generate(self, delay):
        await self.recursive_track(random.randint(0, self.width - 1), random.randint(0, self.height - 1), delay)
