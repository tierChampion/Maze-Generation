from src.maze import Maze
import pygame
import random
import asyncio

vec = pygame.math.Vector2


class SideWinderMaze(Maze):
    def __init__(self, width, height, lateral_dir):
        """
        Maze that generates itself using the Sidewinder algorithm.

        :param width: width in cells of the maze
        :param height: height in cells of the maze
        :param lateral_dir: direction to carve sideways
        """

        super().__init__(width, height)
        directions = ["E", "W"]

        if lateral_dir not in directions:
            print("\n\033[31mERROR: The lateral direction for the Sidewinder is wrong. "
                  "It was set to east.\n")
            lateral_dir = "E"

        lateral_id = directions.index(lateral_dir)
        self.dir = lateral_dir
        directions.remove(lateral_dir)
        self.inv = directions[0]
        deltas = [1, -1]
        self.dx = deltas[lateral_id]

    async def generate(self, delay):
        """
        Generate a maze with the Sidewinder algorithm.
        Row by row, decide to carve sideways or downward. If the decision is to carve sideways,
        add the carved cell to a list and if the decision is to carve downwards, choose a random cell in the list,
        carve a path downward from that cell and clear the list.

        :param delay: time in seconds to wait for every step
        """

        for y in range(self.height):
            run = []
            for x in range(self.width):
                row_pos = self.width - x - 1 if self.dir == "W" else x
                cell = self.get_cell_2d(row_pos, y)
                run.append(cell)

                # Deal with the specific edge cases that limit possibilities
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

                # Move either sideways or down
                if move == 1:
                    cell.walls.remove(self.dir)
                    side_cell = self.get_cell_2d(row_pos + self.dx, y)
                    side_cell.walls.remove(self.inv)
                    self.modified.add(cell)
                    self.modified.add(side_cell)
                elif move == 0:
                    lower_cell = run[random.randint(0, len(run) - 1)]
                    lower_cell.walls.remove("N")
                    top_cell = self.get_cell_2d(lower_cell.col, lower_cell.row - 1)
                    top_cell.walls.remove("S")
                    self.modified.add(lower_cell)
                    self.modified.add(top_cell)
                    run.clear()
                await asyncio.sleep(delay)
