from src.maze import Cell


class GroupElement(Cell):
    def __init__(self, x, y, key):
        """
        Both a Cell in a maze and an element in a group.
        :param x: horizontal position in the maze
        :param y: vertical position in the maze
        :param key: unique key to identify the element
        """

        super().__init__(x, y)
        self.id = key

        # Group in which the element is
        self.group = None

    def is_linked(self, other_cell):
        """
        Determines if two cells are linked together.
        :param other_cell: neighbour cell to test linking with
        :return: whether the cells can be reached
        """

        return self.group == other_cell.group


class Group:
    def __init__(self, elem):
        """
        Collection of elements.
        :param elem: initial element in the group
        """

        # Not ordered and non-repeating set of elements
        self.elements = {elem}
        self.id = elem.id

    def cardinality(self):
        """
        :return: size of the group
        """

        return len(self.elements)

    def append_element(self, elem):
        """
        Add an element to the group.
        :param elem: element to add
        """

        self.elements.add(elem)
        elem.group = self

    def append_elements(self, elems: set):
        """
        Add a set of elements to the group
        :param elems: collection of elements to add
        """

        for elem in elems:
            self.append_element(elem)

    def merge(self, current_row: set, other_group):
        """
        Merge two groups together.
        :param current_row:
        :param other_group:
        """

        self.append_elements(other_group.elements)
        current_row.remove(other_group)

    def clear(self):
        """
        Remove all elements in the group.
        """

        self.elements.clear()
