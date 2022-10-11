from src.maze import Maze
import pygame
import random
import asyncio

vec = pygame.math.Vector2

'''
Iterates throw all the nodes in the graph, adds them to the run set and randomly chooses one of two options:
1- Carve a path either east or west, if possible
2- Choose a random node in the run and carve a path north. Empty run. 
Much like the Binary Tree algorithm, this algorithm has a long path, but this time only on the north wall.
However, the Side-Winder generated mazes don't have a strong diagonal bias.
'''


class SideWinderMaze(Maze):
    def __init__(self, width, height, lateral_dir):
        super().__init__(width, height)
        directions = ["E", "W"]
        lateral_id = directions.index(lateral_dir)
        self.dir = lateral_dir
        directions.remove(lateral_dir)
        self.inv = directions[0]
        deltas = [1, -1]
        self.dx = deltas[lateral_id]

    async def generate(self, delay):
        for y in range(self.height):
            run = []
            for x in range(self.width):
                row_pos = self.width - x - 1 if self.dir == "W" else x
                cell = self.get_cell(row_pos, y)
                run.append(cell)
                if y == 0 and (row_pos == self.width - 1 and self.dir == "E" or
                               row_pos == 0 and self.dir == "W"):
                    continue
                elif y == 0:
                    move = 1
                elif row_pos + self.dx < 0 or \
                        row_pos + self.dx > self.width - 1:
                    move = 0
                else:
                    move = random.randint(0, 1)
                if move == 1:
                    cell.walls.remove(self.dir)
                    side_cell = self.get_cell(row_pos + self.dx, y)
                    side_cell.walls.remove(self.inv)
                    self.modified.add(cell)
                    self.modified.add(side_cell)
                elif move == 0:
                    lower_cell = run[random.randint(0, len(run) - 1)]
                    lower_cell.walls.remove("N")
                    top_cell = self.get_cell(lower_cell.col, lower_cell.row - 1)
                    top_cell.walls.remove("S")
                    self.modified.add(lower_cell)
                    self.modified.add(top_cell)
                    run.clear()
                await asyncio.sleep(delay)
