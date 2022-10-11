from src.maze import Maze, Cell
import pygame
import random
import asyncio

'''
Put each cell of the first row in a different set, then randomly join cells next to each other
if they aren't in the same set. Then randomly create paths downward to the next row, minimum one path per
set. Put any lone cell in that row in it's own set. Continue for all rows, until you reach the last row and then
you don't need to add a vertical path. This is one of the fastest algorithms to make mazes. 
'''


class Group:
    def __init__(self, elem):
        self.elements = {elem}
        self.id = elem.id
        self.sub_groups = {self.id}

    def cardinality(self):
        return len(self.elements)

    def append_element(self, elem):
        self.elements.add(elem)
        elem.set = self
        self.sub_groups.add(elem.id)

    def merge(self, current_row: set, other_group):

        # Set the id to the oldest group
        if other_group.id < self.id:
            self.id = other_group.id
        else:
            other_group.id = self.id

        # Change the set of the elements
        for element in other_group.elements:
            element.set = self
        self.elements = other_group.elements.union(self.elements)
        self.sub_groups = other_group.sub_groups.union(self.sub_groups)
        current_row.remove(other_group)

    def clear(self):
        self.elements.clear()


class GroupElement(Cell):
    def __init__(self, x, y, index):
        super().__init__(x, y)
        self.id = index
        self.set = None

    def assign_set(self, group):
        group.append_element(self)

    def get_groups(self):
        if self.set:
            return self.set.elements
        else:
            return [self]

    def is_linked(self, elem):
        return self.set == elem.set

    def link(self, elem):
        if not elem.is_linked(self):
            self.set.append_element(elem)


class EllerMaze(Maze):
    def __init__(self, width, height, side_factor, down_factor):
        super().__init__(width, height)
        self.side_factor = side_factor
        self.down_factor = down_factor

    def empty_grid(self):
        grid = []
        set_count = 0
        for y in range(self.height):
            for x in range(self.width):
                cell = GroupElement(x, y, set_count)
                set_count += 1
                grid.append(cell)
        return grid

    async def generate(self, delay: float):

        """
        Generate a maze with Eller's Algorithm.
        Row by row, make group containing cells. Gradually merge groups and expand them down.
        At the end, all groups merge into a single one, which means that every cell is connected
        to every other cell.

        :param delay: time in seconds to wait for every step
        """

        for y in range(self.height):

            # Init row groups
            current_sets = set()
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if not cell.set:
                    cell.assign_set(Group(cell))
                current_sets.add(cell.set)

            # Fuse groups
            for x in range(self.width - 1):
                cell = self.get_cell(x, y)
                next_cell = self.get_cell(x + 1, y)
                if not cell.is_linked(next_cell):
                    to_link = random.random() > self.side_factor or y == self.height - 1
                    if to_link:
                        cell.set.merge(current_sets, next_cell.set)
                        cell.walls.remove("E")
                        next_cell.walls.remove("W")
                        self.modified.add(cell)
                        self.modified.add(next_cell)
                        await asyncio.sleep(delay)

            # Branch downwards at least once per group
            if y < self.height - 1:
                for group in current_sets:

                    # Elements in the lower row that where added
                    extended_set = set()
                    elem_list = list(group.elements)
                    has_path_down = False

                    for i in range(len(elem_list)):
                        # Make a path down or not. Has to if there are no path in all other elements
                        make_path = (random.random() > self.down_factor) or \
                                    (not has_path_down and i == len(elem_list) - 1)
                        if make_path:
                            has_path_down = True

                            element = elem_list[i]
                            lower_element = self.get_cell(element.col, element.row + 1)

                            element.walls.remove("S")
                            lower_element.walls.remove("N")

                            # Add new element to group
                            element.link(lower_element)
                            extended_set.add(lower_element)
                            self.modified.add(element)
                            self.modified.add(lower_element)
                            await asyncio.sleep(delay)

                    # Only keep the next row of elements
                    group.elements.clear()
                    group.elements.update(extended_set)
