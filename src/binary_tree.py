from src.maze import Maze
import pygame
import random
import asyncio


class BinaryTreeMaze(Maze):

    def __init__(self, width: int, height: int, north_or_south: str, east_or_west: str):
        """
        Maze that generates itself using the binary tree algorithm.

        :param width: Width in cells of the maze
        :param height: Height in cells of the maze
        :param north_or_south: Direction to carve in the vertical direction. Either "N" or "S"
        :param east_or_west: Direction to carve in the horizontal direction. Either "E" or "W"
        """

        super().__init__(width, height)
        directions = ["E", "W", "N", "S"]
        self.dirs = [east_or_west]
        directions.remove(east_or_west)
        self.invs = [directions[0]]

        self.dirs.append(north_or_south)
        directions.remove(north_or_south)
        self.invs.append(directions[1])

        self.dx = [2 * (east_or_west == "E") - 1, 0]
        self.dy = [0, 2 * (north_or_south == "S") - 1]

    async def generate(self, delay: float):
        """
        Generate a maze with the binary tree algorithm.
        Choose one horizontal direction and one vertical direction. For every cell, either carve in the horizontal
        direction or the vertical direction or neither. Creates a strong bias towards one of the diagonals.

        :param delay: time in seconds to wait for every step
        """

        for cell in self.grid:
            x = cell.col
            y = cell.row

            # Choose a direction to carve. Try other direction if needed or don't carve at all
            index = random.randint(0, 1)
            for i in range(2):
                if (x + self.dx[index] < 0 or x + self.dx[index] > self.width - 1 or y + self.dy[index] < 0 or y +
                        self.dy[index] > self.height - 1):
                    if i == 1:
                        index = -1
                    else:
                        index = (index + 1) % 2

            if index == -1:
                continue

            # Remove needed wall
            cell.walls.remove(self.dirs[index])
            other_cell = self.get_cell_2d(x + self.dx[index], y + self.dy[index])
            other_cell.walls.remove(self.invs[index])
            self.modified.add(cell)
            self.modified.add(other_cell)
            await asyncio.sleep(delay)
