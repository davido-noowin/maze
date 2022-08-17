# maze_solver.py
#
# the class that solves the completed maze

import pygame
from constants import *


class Solver:
    '''
    The Solver class is the maze solver. Once the maze has been generated, it will use a depth-first
    algorithm to traverse the maze and find the end of the maze.
    '''
    def find_cell(column, row) -> int:
        '''
        Uses an equation to find the position of a cell in a 1D array mapped to a 2D array

        :returns:
            int
        '''
        return column + row * cols

    def __init__(self, width: int, height: int, grid: list, screen: pygame.display):
        '''
        Initializes the Solver class. It will first generate an empty array with 0 signifying that no cells have been
        visited. It will then set the current cell that we are on to the first cell in our maze. We create empty lists for
        our stack which is needed for the algorithm and a list for movement so that we can see it on the screen.

        :params:
            width - int - width of the maze
            height - int - height of the maze
            grid - list - the maze that holds the cells
            screen - pygame.display
        '''
        # creates an empty maze that is all 0, signifying that cells are all unvisited
        self.maze = [0 for _ in grid]

        self.width = width
        self.height = height
        self.grid = grid

        self.x_start = 0
        self.y_start = 0

        # the end of the maze will be the bottom right corner, while the maze starts at (0,0)
        self.x_end = width - 1
        self.y_end = height - 1
        
        self.screen = screen


        self.current = self.grid[0]
        self.movement = []
        self.stack = []


    def __str__(self) -> str:
        '''
        Returns a string that contains the visited/unvisited cells

        :returns:
            str
        '''
        return f'{self.maze}'


    def draw_cell(self, x, y) -> None:
        '''
        Draws the cell that the solver is currently on. If the solver is on cell (1,1). then there will be a
        blue circle at cell (1,1).

        :params:
            x - int - the x position of the cell
            y - int - the y position of the cell
        '''
        width = x * TILE
        height = y * TILE

        pygame.draw.rect(self.screen, (135, 206, 235), (width+TILE//4, height+TILE//4, TILE // 2, TILE // 2), border_radius=15)

    
    def is_legal(self, x, y) -> bool:
        '''
        Returns True or False depending on whether or not the given cell is within the boundaries of the maze.

        :params:
            x - int - the x position of the cell
            y - int - the y position of the cell

        :returns: 
            True or False
        '''
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        else:
            return True

    
    def check_up(self) -> bool:
        '''
        A function that looks in the up direction and returns true if: 
            1) the next cell is within legal bounds of the maze
            2) the next cell has not been visited yet
            3) the current cell has a path leading to the next cell

        :returns:
            bool
        '''
        if self.is_legal(self.current.x, self.current.y-1):
            # if it hasn't been visited and you can travel in that direction, then return True
            if (not self.maze[Solver.find_cell(self.current.x, self.current.y-1)]) and (not self.current.walls['up']):
                return True
            else:
                return False
        else:
            return False


    def check_right(self) -> bool:
        '''
        A function that looks in the right direction and returns true if: 
            1) the next cell is within legal bounds of the maze
            2) the next cell has not been visited yet
            3) the current cell has a path leading to the next cell

        :returns:
            bool
        '''
        if self.is_legal(self.current.x+1, self.current.y):
            if (not self.maze[Solver.find_cell(self.current.x+1, self.current.y)]) and (not self.current.walls['right']):
                return True
            else:
                return False
        else:
            return False


    def check_left(self) -> bool:
        '''
        A function that looks in the left direction and returns true if: 
            1) the next cell is within legal bounds of the maze
            2) the next cell has not been visited yet
            3) the current cell has a path leading to the next cell

        :returns:
            bool
        '''
        if self.is_legal(self.current.x-1, self.current.y):
            if (not self.maze[Solver.find_cell(self.current.x-1, self.current.y)]) and (not self.current.walls['left']):
                return True
            else:
                return False
        else:
            return False


    def check_down(self) -> bool:
        '''
        A function that looks in the down direction and returns true if: 
            1) the next cell is within legal bounds of the maze
            2) the next cell has not been visited yet
            3) the current cell has a path leading to the next cell

        :returns:
            bool
        '''
        if self.is_legal(self.current.x, self.current.y+1):
            if (not self.maze[Solver.find_cell(self.current.x, self.current.y+1)]) and (not self.current.walls['down']):
                return True
            else:
                return False
        else:
            return False

    
    def move(self) -> None:
        '''
        The main algorithm of the Solver class. It employs a depth-first traversal algorithm that will check first if it is solved. 
        After it will take the current cell and mark it as visited then put it onto the stack. It will then check any adjacent cells of the
        current cell and put it onto the stack. If it hits a dead end, it will pop that cell from the stack and backtrack, picking another adjacent cell.
        '''
        if self.is_solved():
            pass
        else:
            if (not self.maze[Solver.find_cell(self.current.x, self.current.y)]):
                self.maze[Solver.find_cell(self.current.x, self.current.y)] = 1 # marks it as visited

                if self.current not in self.stack:
                    self.stack.append(self.current)
                    self.movement.append(self.current) # used for drawing

                next_cell = False
                if self.check_right():
                    next_cell = self.grid[Solver.find_cell(self.current.x+1, self.current.y)]
                elif self.check_left():
                    next_cell = self.grid[Solver.find_cell(self.current.x-1, self.current.y)]
                elif self.check_down():
                    next_cell = self.grid[Solver.find_cell(self.current.x, self.current.y+1)]
                elif self.check_up():
                    next_cell = self.grid[Solver.find_cell(self.current.x, self.current.y-1)]

                if next_cell: # if the cell we check is valid and does not return False then we make it the current cell
                    self.current = next_cell
            else:
                self.stack.pop()
                self.movement.pop()
                self.current = self.stack[-1] # backtrack to the previous cell
                self.maze[Solver.find_cell(self.current.x, self.current.y)] = 0 # marks it as unvisited


    def build(self) -> None:
        '''
        Goes through the movement list and draws all cells that are on the path to the end of the maze
        '''
        for cells in self.movement:
            self.draw_cell(cells.x, cells.y)


    def is_solved(self) -> bool:
        '''
        Returns true or false depending if the the ending cell has been reached

        :returns:
            bool
        '''
        return True if self.maze[Solver.find_cell(self.x_end, self.y_end)] else False