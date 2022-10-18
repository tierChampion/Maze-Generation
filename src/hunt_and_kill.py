from src.maze import Maze
import random
import asyncio


class HuntAndKillMaze(Maze):
    def __init__(self, width, height):
        """
        Maze that generates itself using the Hunt and Kill algorithm.

        :param width: width in cells of the maze
        :param height: height in cells of the maze
        """

        super().__init__(width, height)
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]

    async def walk(self, x, y, delay):
        """
        Carve a path with a random walk.

        :param x: lateral position to start from
        :param y: vertical position to start from
        :param delay: time in seconds to wait every frame
        """

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
                        self.modified.add(current_cell)
                        self.modified.add(next_cell)
                        current_cell = next_cell
                        current_cell.visited = True
            if current_cell == old_cell:
                can_walk = False
            await asyncio.sleep(delay)

    async def hunt(self):
        """
        Select a new random starting point.

        :return: new position
        """

        vert = list(range(self.height))
        lat = list(range(self.width))

        random.shuffle(vert)
        random.shuffle(lat)

        for y in vert:
            for x in lat:
                if not self.get_cell_2d(x, y).visited:
                    return x, y
        return -1, -1

    async def generate(self, delay):
        """
        Generate a maze with the Hunt and Kill algorithm.
        Start at a random point in the maze and random walk until stuck in a
        dead-end. Repeat with new starting points making sure to connect them to a nearby walk
        if possible until no paths are possible.

        :param delay: time to wait for in seconds
        """

        current_x = random.randint(0, self.width - 1)
        current_y = random.randint(0, self.height - 1)
        can_generate = True
        while can_generate:
            # Random walk and find new starting point
            await self.walk(current_x, current_y, delay)
            current_x, current_y = await self.hunt()

            if current_x == current_y == -1:
                can_generate = False
            else:
                found_neighbour = False

                # Connect new origin if possible
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
