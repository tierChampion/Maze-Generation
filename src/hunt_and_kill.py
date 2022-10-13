from src.maze import Maze
import pygame
import random
import asyncio

vec = pygame.math.Vector2

'''
Start at a preselected node and go into the 'walk' behaviour, where you perform a random walk, carving a path along 
the way. When it is impossible to find an available neighbour, go into the 'hunt' behaviour, where you iterate through 
the graph to find an available node from where to start over. Similarly to the Recursive-Backtracker, this algorithm 
creates very long paths.
'''


class HuntAndKillMaze(Maze):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]

    async def walk(self, x, y, delay):
        current_cell = self.get_cell_2d(x, y)
        current_cell.visited = True
        can_walk = True
        while can_walk:
            old_cell = current_cell
            data = list(zip(self.directions, self.dx, self.dy, self.inverses))
            random.shuffle(data)
            self.directions, self.dx, self.dy, self.inverses = zip(*data)
            for idx, direction in enumerate(self.directions):
                new_x = current_cell.col + self.dx[idx]
                new_y = current_cell.row + self.dy[idx]
                if self.width > new_x >= 0 and self.height > new_y >= 0:
                    if not self.get_cell_2d(new_x, new_y).visited:
                        current_cell.walls.remove(direction)
                        next_cell = self.get_cell_2d(new_x, new_y)
                        next_cell.walls.remove(self.inverses[idx])
                        self.modified.append(current_cell)
                        self.modified.append(next_cell)
                        current_cell = next_cell
                        current_cell.visited = True
            if current_cell == old_cell:
                can_walk = False
            await asyncio.sleep(delay)

    async def hunt(self):
        for y in range(self.height):
            for x in range(self.width):
                if not self.get_cell_2d(x, y).visited:
                    return x, y
        return None, None

    async def generate(self, delay):
        current_x = random.randint(0, self.width - 1)
        current_y = random.randint(0, self.height - 1)
        can_generate = True
        while can_generate:
            await self.walk(current_x, current_y, delay)
            current_x, current_y = await self.hunt()
            if not current_x and not current_y:
                can_generate = False
            else:
                found_neighbour = False
                for idx, direction in enumerate(self.directions):
                    new_x = current_x + self.dx[idx]
                    new_y = current_y + self.dy[idx]
                    if self.width > new_x >= 0 and self.height > new_y >= 0:
                        if self.get_cell_2d(new_x, new_y).visited:
                            self.get_cell_2d(current_x, current_y).walls.remove(direction)
                            self.get_cell_2d(new_x, new_y).walls.remove(self.inverses[idx])
                            self.modified.add(self.get_cell_2d(current_x, current_y))
                            self.modified.add(self.get_cell_2d(new_x, new_y))
                            found_neighbour = True
                    if found_neighbour:
                        break
