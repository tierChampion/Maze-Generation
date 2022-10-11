import asyncio

import pygame

from src.aldous_broder import AldousBroderMaze
from src.binary_tree import BinaryTreeMaze
from src.eller_algorithm import EllerMaze
from src.growing_tree import GrowingTreeMaze
from src.hunt_and_kill import HuntAndKillMaze
from src.kruskal_algorithm import KruskalMaze
from src.pac_man import PacManMaze
from src.primm_algorithm import PrimmMaze
from src.recursive_backtrakcker import RecursiveBackTrackerMaze
from src.recursive_division import RecursiveDivisionMaze
from src.sidewinder import SideWinderMaze

# ADD THE POSSIBILITIES TO CONSTRUCTORS OF BINARY TREE


async def main(maze_type: int):

    screen_dim = 800
    maze_dim = 90

    window = pygame.display.set_mode((screen_dim, screen_dim))
    clock = pygame.time.Clock()

    if maze_type == 0:
        maze = AldousBroderMaze(maze_dim, maze_dim)
    elif maze_type == 1:
        maze = BinaryTreeMaze(maze_dim, maze_dim)
    elif maze_type == 2:
        maze = EllerMaze(maze_dim, maze_dim, 0.5, 0.5)
    elif maze_type == 3:
        maze = GrowingTreeMaze(maze_dim, maze_dim, "Random")
    elif maze_type == 4:
        maze = HuntAndKillMaze(maze_dim, maze_dim)
    elif maze_type == 5:
        maze = KruskalMaze(maze_dim, maze_dim)
    elif maze_type == 6:
        maze = PacManMaze(maze_dim, maze_dim)
    elif maze_type == 7:
        maze = PrimmMaze(maze_dim, maze_dim)
    elif maze_type == 8:
        maze = RecursiveBackTrackerMaze(maze_dim, maze_dim)
    elif maze_type == 9:
        maze = RecursiveDivisionMaze(maze_dim, maze_dim)
    else:
        maze = SideWinderMaze(maze_dim, maze_dim, "E")

    finished = False
    running = True
    delay = 0

    cell_dim = screen_dim / (maze_dim + 2)

    maze.init_render(window, cell_dim)

    while running:
        clock.tick(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        if not finished:
            await asyncio.gather(
                maze.generate(delay),
                maze.render(window, cell_dim, delay)
            )
            maze.init_render(window, cell_dim)
        finished = True
    pygame.quit()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(9))
