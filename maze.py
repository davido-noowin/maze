# maze.py
#
# the maze class that constructs the maze onto the pygame window

import pygame
from random import choice
from cells import Cell
from constants import *


class Maze:
    '''
    The Maze class builds the maze that can be seen in the pygame window. It controls the generation
    and the storage of individual Cells.
    '''
    def __init__(self, maze_width: int, maze_height: int, size: int, win: pygame.display):
        '''
        Initializes the Maze class. Creates a one dimensional grid holding Cell objects. We can use math to transform the 1D array into a 
        2D array to display on the pygame window. Takes in the maze's width, height and size of individual cells to generate the maze.

        :params:
            maze_width - int - width of the maze
            maze_height - int - height of the maze
            size - int - size of the maze cells
            win - pygame.display - display window
        '''
        self.width = maze_width
        
        self.height = maze_height
        self.size = size
        self.win = win

        self.grid = [Cell(col, row, self.size, self.win) for row in range(rows) for col in range(cols)]
        self.current_cell = self.grid[0]
        self.stack = []

    
    def check_cell(self, x: int, y: int) -> bool or Cell:
        '''
        Checks whether or not the given x and y positions are valid and returns that cell based on where it is on the grid.

        :params:
            x - int
            y - int
        
        :returns: Cell or False
        '''
        find_index = lambda x, y : x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        else:
            return self.grid[find_index(x, y)]


    def check_neighbors(self, x, y) -> Cell or bool:
        '''
        Checks whether or not the adjacent cells of the current cell is a legal move. If it is legal, it will be added to the list of possible
        directions to travel and will call the random function to choose the next cell.

        :params:
            x - int
            y - int

        :returns:
            Cell or False
        '''
        cell_storage = []

        up = self.check_cell(x, y - 1)
        right = self.check_cell(x  + 1, y)
        down = self.check_cell(x, y + 1)
        left = self.check_cell(x  - 1, y)

        if up and not up.visited:
            cell_storage.append(up)
        if right and not right.visited:
            cell_storage.append(right)
        if down and not down.visited:
            cell_storage.append(down)
        if left and not left.visited:
            cell_storage.append(left)

        return choice(cell_storage) if cell_storage else False


    def remove_walls(self, current, next) -> None:
        '''
        Calculates the change in x and y positions from the current and next cell and uses that to determine which walls to knock down.
        dx sigifies a change in left or right walls, why dy signnifies a change in up or down walls.

        :params:
            current - Cell - the current cell that is selected
            next - Cell - the next cell that is being compared against
        '''
        dx = current.x - next.x
        dy = current.y - next.y

        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False

        if dy == 1:
            current.walls['up'] = False
            next.walls['down'] = False
        elif dy == -1:
            current.walls['down'] = False
            next.walls['up'] = False


    def construct(self) -> None:
        '''
        The main algorithm that generates the maze. The algorithm will construct a list of cells and draw it
        onto the screen for the user. Then it will use a depth-first algorithm to mark each cell as visited and randomly 
        choose adjacent cells to mark as visited. While that is happening, it will also randomly choose walls to knock down 
        to make connections possible.
        '''
        [cell.construct() for cell in self.grid]
        self.current_cell.visited = True

        if not self.is_done():
            self.current_cell.draw_current_cell()

        next_cell = self.check_neighbors(self.current_cell.x, self.current_cell.y)
        if next_cell:
            next_cell.visited = True
            self.stack.append(self.current_cell)
            self.remove_walls(self.current_cell, next_cell)
            self.current_cell = next_cell
        elif self.stack:
            self.current_cell = self.stack.pop()

    
    def get_grid(self) -> list:
        '''
        Returns the grid of cells that was constructed from the given Maze class

        :returns: 
            list
        '''
        return self.grid

    
    def is_done(self) -> bool:
        '''
        Returns a boolean value depending if all cells in the grid were visited

        :returns: 
            True or False
        '''
        return True if all([bool.visited for bool in self.grid]) else False
