from src.maze import Maze
import random
import asyncio


class PrimmMaze(Maze):
    def __init__(self, width, height):
        """
        Maze that generates itself using Primm's algorithm.

        :param width: width in cells of the maze
        :param height: height in cells of the maze
        """

        super().__init__(width, height)
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
        """
        Generate a maze with Primm's algorithm.
        Start with a list with a single random cell inside it. For every step, choose random cell in the list
        and carve to one of its neighbour that wasn't visited before. If the cell doesn't have any more
        neighbours, remove it from the list. Repeat this procedure until the list is empty.

        :param: delay: time to wait for in seconds
        """

        V = []
        random_cell = self.get_cell_2d(random.randrange(0, self.width - 1), random.randrange(0, self.height - 1))
        random_cell.visited = True
        V.append(random_cell)
        while V:
            selected_cell = V[random.randint(0, len(V) - 1)]
            selected_cell.visited = True
            available_neighbour = self.carve_to_unvisited(selected_cell)
            if not available_neighbour:
                V.remove(selected_cell)
                continue
            available_neighbour.visited = True
            V.append(available_neighbour)
            await asyncio.sleep(delay)
