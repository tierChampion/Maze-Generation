from src.maze import Maze, Cell
import pygame
import random
import asyncio

vec = pygame.math.Vector2

'''
Put all possible edges in a set. Every cell starts in a separate tree. Select edges from the set at random and join
the two trees separated by that edge if they are from different trees. This algorithm gives a result similar to 
Primm's algorithm, a lot of small paths
'''


class TreeCell(Cell):
    def __init__(self, x, y, root):
        super().__init__(x, y)
        self.root = root


class Tree:
    def __init__(self, cell):
        self.cells = [cell]
        self.id = cell.root

    def fusion(self, trees: list, cell: TreeCell):
        """
        Merge the cells in the same tree as cell to this tree.
        :param trees: list of all the trees
        :param cell: cell of the tree to merge to this tree
        """

        other_tree = next(tree for tree in trees if tree.id == cell.root)
        for cell in other_tree.cells:
            cell.root = self.id
        self.cells.extend(other_tree.cells)
        trees.remove(other_tree)


class KruskalMaze(Maze):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.directions = ["E", "W", "N", "S"]
        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, -1, 1]
        self.inverses = ["W", "E", "S", "N"]

    def empty_grid(self):
        grid = []
        tree = 0
        for y in range(self.height):
            for x in range(self.width):
                cell = TreeCell(x, y, tree)
                tree += 1
                grid.append(cell)
        return grid

    def get_edges(self):
        edges = []
        for cell in self.grid:
            edge1 = [cell.col, cell.row, self.directions.index("E")]
            edge2 = [cell.col, cell.row, self.directions.index("S")]
            if cell.col < self.width - 1:
                edges.append(edge1)
            if cell.row < self.height - 1:
                edges.append(edge2)
        return edges

    def get_trees(self):
        trees = []
        for cell in self.grid:
            tree = Tree(cell)
            trees.append(tree)
        return trees

    async def generate(self, delay):
        edges = self.get_edges()
        trees = self.get_trees()
        random.shuffle(edges)
        while edges:
            selected_edge = edges.pop()
            cell1 = self.get_cell_2d(selected_edge[0], selected_edge[1])
            i = selected_edge[2]
            cell2 = self.get_cell_2d(cell1.col + self.dx[i], cell1.row + self.dy[i])
            if cell1.root == cell2.root:
                continue
            tree = next(tree for tree in trees if tree.id == cell1.root)
            tree.fusion(trees, cell2)
            cell1.walls.remove(self.directions[i])
            cell2.walls.remove(self.inverses[i])
            self.modified.add(cell1)
            self.modified.add(cell2)
            await asyncio.sleep(delay)
