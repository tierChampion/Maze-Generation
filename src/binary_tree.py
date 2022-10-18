from src.maze import Maze
import random
import asyncio


class BinaryTreeMaze(Maze):

    def __init__(self, width: int, height: int, dirs: tuple):
        """
        Maze that generates itself using the binary tree algorithm.

        :param width: width in cells of the maze
        :param height: height in cells of the maze
        :param dirs: a pair of directions. The first element is the E or W
        and the second one is N or S
        """

        super().__init__(width, height)
        directions = ["E", "W", "N", "S"]

        if dirs[0] != "E" or "W":
            print("\n\033[31mERROR: The lateral direction for the Binary Tree is wrong. "
                  "It was set to east.\n")
            dirs = ("E", dirs[1])
        if dirs[1] != "N" or "S":
            print("\n\033[31mERROR: The vertical direction for the Binary tree is wrong. "
                  "It was set to south.\n")
            dirs = (dirs[0], "S")


        self.dirs = [dirs[0]]
        directions.remove(dirs[0])
        self.invs = [directions[0]]

        self.dirs.append(dirs[1])
        directions.remove(dirs[1])
        self.invs.append(directions[1])

        self.dx = [2 * (dirs[0] == "E") - 1, 0]
        self.dy = [0, 2 * (dirs[1] == "S") - 1]

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
