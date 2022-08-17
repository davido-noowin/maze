# interface.py 
# 
# run this file to generate the maze
# 'LCTRL' to reset the maze generation
# 'space' to solve the maze
#

import pygame
import sys
from maze import Maze
from maze_solver import Solver
from constants import *


# SCREEN
WIN = pygame.display.set_mode(RES) # RES imported from constants.py
pygame.display.set_caption('Maze Generator')
FPS = 60


def main() -> None:
    '''
    Runs the program and starts up the pygame window.
    '''
    clock = pygame.time.Clock()
    m = Maze(rows, cols, TILE, WIN) # initialize the Maze class
    is_solving = False # a flag indicating that the maze is not done generating yet

    while True:
        WIN.fill(WHITE)

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    main()
                if event.key == pygame.K_SPACE and m.is_done() and not is_solving:
                    is_solving = True # once we are done generating we can set this flag to True and start solving
                    solve = Solver(cols, rows, m.get_grid(), WIN) # intialize the Solver class

        m.construct()

        if is_solving:
            solve.move() # the algorithm
            solve.build() # the visual

        pygame.display.update()


if __name__ == '__main__':
    main()