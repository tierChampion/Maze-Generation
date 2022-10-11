from src.maze import Maze
import pygame
import random
import asyncio

vec = pygame.math.Vector2

'''
Probably the simplest algorithm. Iterate throw all the nodes in the graph and carve a passage in either 
of two pre-selected directions, if it is possible. This algorithm creates two long paths on the sides
of the selected directions and as strong diagonal bias.
'''


class BinaryTreeMaze(Maze):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]

    async def generate(self, possibilities, delay):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                directions = []
                for p in possibilities:
                    directions.append(p) # Array of directions
                index = directions[random.randint(0, len(directions) - 1)]
                while (x + self.dx[index] < 0 or x + self.dx[index] > self.width - 1 or y + self.dy[index] < 0 or y +
                        self.dy[index] > self.height - 1):
                    directions.remove(index)
                    if not directions:
                        break
                    index = directions[random.randint(0, len(directions) - 1)]
                if not directions:
                    continue
                cell.walls.remove(self.directions[index])
                other_cell = self.get_cell(x + self.dx[index], y + self.dy[index])
                other_cell.walls.remove(self.inverses[index])
                self.modified.add(cell)
                self.modified.add(other_cell)
                await asyncio.sleep(delay)
