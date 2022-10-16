from src.maze import Maze
from src.group import GroupElement, Group
import random
import asyncio


class EllerMaze(Maze):
    def __init__(self, width, height, side_factor, down_factor):
        """
        Maze that generates itself using Eller's Algorithm.
        :param width: width in cells of the maze
        :param height: height in cells of the maze
        :param side_factor: probability to merge with a lateral neighbour
        :param down_factor: probability to extend the group downwards
        """

        super().__init__(width, height)
        self.side_factor = side_factor
        self.down_factor = down_factor

    def empty_grid(self):
        grid = []
        group_count = 0
        for y in range(self.height):
            for x in range(self.width):
                cell = GroupElement(x, y, group_count)
                group_count += 1
                grid.append(cell)
        return grid

    async def generate(self, delay: float):
        """
        Generate a maze with Eller's Algorithm.
        Row by row, make group containing cells or elements. Gradually merge groups and expand them down.
        At the end, all groups merge into a single one, which means that every cell is connected
        to every other cell.
        :param delay: time in seconds to wait for every step
        """

        for y in range(self.height):

            # Init row groups
            current_groups = set()
            for x in range(self.width):
                cell = self.get_cell_2d(x, y)
                if not cell.group:
                    new_group = Group(cell)
                    new_group.append_element(cell)
                current_groups.add(cell.group)

            # Fuse groups laterally
            for x in range(self.width - 1):
                cell = self.get_cell_2d(x, y)
                next_cell = self.get_cell_2d(x + 1, y)
                if not cell.is_linked(next_cell):
                    to_link = random.random() > self.side_factor or y == self.height - 1
                    if to_link:
                        cell.group.merge(current_groups, next_cell.group)
                        cell.walls.remove("E")
                        next_cell.walls.remove("W")
                        self.modified.add(cell)
                        self.modified.add(next_cell)
                        await asyncio.sleep(delay)

            # Branch downwards at least once per group
            if y < self.height - 1:
                for group in current_groups:

                    # Elements in the lower row that where added
                    new_elements = set()
                    elem_list = list(group.elements)
                    has_path_down = False

                    for i in range(len(elem_list)):
                        # Make a path down or not. Has to if there are no path in all other elements
                        make_path = (random.random() > self.down_factor) or \
                                    (not has_path_down and i == len(elem_list) - 1)
                        if make_path:
                            has_path_down = True

                            element = elem_list[i]
                            lower_element = self.get_cell_2d(element.col, element.row + 1)

                            element.walls.remove("S")
                            lower_element.walls.remove("N")

                            # Add new element to group
                            element.group.append_element(lower_element)
                            new_elements.add(lower_element)
                            self.modified.add(element)
                            self.modified.add(lower_element)
                            await asyncio.sleep(delay)

                    # Only keep the next row of elements
                    group.clear()
                    group.append_elements(new_elements)
