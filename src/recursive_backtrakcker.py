from src.maze import Maze
import random
import asyncio


class RecursiveBackTrackerMaze(Maze):
    def __init__(self, width, height):
        """
        Maze that generates itself using the Recursive Backtracker algorithm

        :param width: width in cells of the maze
        :param height: height in cells of the maze
        """

        super().__init__(width, height)
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]

    async def generate(self, delay):
        """
        Generate a maze with the Recursive Backtracker algorithm.
        Start with a random cell in a stack. Remove the top cell in the stack and carve to a random neighbour.
        If other possible neighbours remain, add back the cell in the stack. Add the carved neighbour to the
        top of the stack and repeat the steps until the stack is empty.

        :param delay: time to wait for in seconds
        """

        pos_stack = [(random.randint(0, self.width - 1), random.randint(0, self.height - 1))]

        self.get_cell_2d(pos_stack[0][0], pos_stack[0][1]).visited = True

        while pos_stack:

            current_x, current_y = pos_stack.pop()

            data = list(zip(self.directions, self.dx, self.dy, self.inverses))
            random.shuffle(data)
            self.directions, self.dx, self.dy, self.inverses = zip(*data)
            for idx, direction in enumerate(self.directions):
                new_x = current_x + self.dx[idx]
                new_y = current_y + self.dy[idx]
                if not (new_x < 0 or new_x > self.width - 1 or new_y < 0 or new_y > self.height - 1):
                    if not self.get_cell_2d(new_x, new_y).visited:
                        self.get_cell_2d(new_x, new_y).visited = True
                        self.get_cell_2d(current_x, current_y).walls.remove(self.directions[idx])
                        self.get_cell_2d(new_x, new_y).walls.remove(self.inverses[idx])
                        self.modified.add(self.get_cell_2d(current_x, current_y))
                        self.modified.add(self.get_cell_2d(new_x, new_y))
                        if idx != 3:
                            pos_stack.append((current_x, current_y))
                        pos_stack.append((new_x, new_y))
                        await asyncio.sleep(delay)
                        break
