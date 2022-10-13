from src.maze import Maze
import pygame
import random
import asyncio

vec = pygame.math.Vector2

'''
Start with a set C, in which you put a random vertex. You then select a vertex in C, carve a path between it and an 
available neighbour. If there isn't an available neighbour, remove the vertex from C. Depending on the method of 
selection, The maze generation behaves differently. Randomly, it is exactly like Primm's Algorithm and if 
you pick the newest vertex in C, it is exactly like the Recursive-Backtracker Algorithm.
'''


def choose_cell(cells: list, method: str):
    if method == "Oldest":
        return cells[0]
    elif method == "Newest":
        return cells[-1]
    else:
        return cells[random.randint(0, len(cells) - 1)]


class GrowingTreeMaze(Maze):
    def __init__(self, width, height, method):
        super().__init__(width, height)
        self.method = method
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]

    def carve_to_unvisited(self, cell):
        data = list(zip(self.directions, self.dx, self.dy, self.inverses))
        random.shuffle(data)
        self.directions, self.dx, self.dy, self.inverses = zip(*data)
        for d in range(len(self.directions)):
            new_x = cell.col + self.dx[d]
            new_y = cell.row + self.dy[d]
            if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.width:
                continue
            new_cell = self.get_cell_2d(new_x, new_y)
            if new_cell.visited:
                continue
            cell.walls.remove(self.directions[d])
            new_cell.walls.remove(self.inverses[d])
            self.modified.add(cell)
            self.modified.add(new_cell)
            return new_cell
        return None

    async def generate(self, delay):
        C = []
        random_cell = self.get_cell_2d(random.randrange(0, self.width - 1), random.randrange(0, self.height - 1))
        random_cell.visited = True
        C.append(random_cell)
        while C:
            selected_cell = choose_cell(C, self.method)
            selected_cell.visited = True
            available_neighbour = self.carve_to_unvisited(selected_cell)
            if not available_neighbour:
                C.remove(selected_cell)
                continue
            available_neighbour.visited = True
            C.append(available_neighbour)
            await asyncio.sleep(delay)
