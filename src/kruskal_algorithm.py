from src.maze import Maze
from src.group import Group, GroupElement
import random
import asyncio


class KruskalMaze(Maze):
    def __init__(self, width, height):
        """
        Maze that generates itself using Kruskall's algorithm.

        :param width: width in cells of the maze
        :param height: height in cells of the maze
        """

        super().__init__(width, height)
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]

    def empty_grid(self):
        grid = []
        group_id = 0
        for y in range(self.height):
            for x in range(self.width):
                cell = GroupElement(x, y, group_id)
                group_id += 1
                grid.append(cell)
        return grid

    def get_edges(self):
        """
        Get all the edges in the maze.

        :return: edges
        """

        edges = []
        for cell in self.grid:
            edge1 = [cell.col, cell.row, self.directions.index("E")]
            edge2 = [cell.col, cell.row, self.directions.index("S")]
            if cell.col < self.width - 1:
                edges.append(edge1)
            if cell.row < self.height - 1:
                edges.append(edge2)
        return edges

    def get_groups(self):
        """
        Get all the groups in the maze.

        :return: groups
        """

        groups = []
        for cell in self.grid:
            group = Group(cell)
            cell.group = group
            groups.append(group)
        return groups

    async def generate(self, delay):
        """
        Generate the maze using Kruskall's algorithm.
        Place every cell into a group. Randomly select an edge and merge the two groups on
        either side of the edge if they are different. Repeat this until there are no edges
        that haven't been checked.

        :param delay: time to wait for in seconds
        """

        edges = self.get_edges()
        groups = self.get_groups()
        random.shuffle(edges)
        while edges:
            selected_edge = edges.pop()
            cell = self.get_cell_2d(selected_edge[0], selected_edge[1])
            dir_id = selected_edge[2]
            other_cell = self.get_cell_2d(cell.col + self.dx[dir_id], cell.row + self.dy[dir_id])
            if cell.group == other_cell.group:
                continue
            group = cell.group
            group.merge(groups, other_cell.group)
            cell.walls.remove(self.directions[dir_id])
            other_cell.walls.remove(self.inverses[dir_id])
            self.modified.add(cell)
            self.modified.add(other_cell)
            await asyncio.sleep(delay)
