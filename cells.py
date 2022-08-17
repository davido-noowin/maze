# cells.py
#
# this serves as a module that stores 'cell' classes that form the grid of our maze

import pygame
from random import choice
from constants import *


class Cell:
    '''
    The Cell class constructs the individual squares in the maze and holds properties for each cell like its x and y position, its size,
    if its walls still exist, and if it has been visited.
    '''
    def __init__(self, x: int, y: int, size: int, window: pygame.display):
        '''
        Initializes the Cell class and its properties.

        :params:
            x - int - x position of Cell
            y - int - y position of Cell
            size - int - the size of the cell
            window - pygame.display - the window to draw the cell on
        '''
        self.x = x
        self.y = y
        self.size = size

        self.visited = False

        self.walls = {
            'up' : True,
            'down' : True,
            'left' : True,
            'right' : True
        }

        self.win = window

    
    def __str__(self) -> str:
        '''
        Returns the x and y position of the cell

        :returns: 
            str
        '''
        return f'Cell: ({self.x}, {self.y})'

    
    def __repr__(self) -> str:
        '''
        Returns the x,y and wall dictionary of the cell

        :returns:
            str
        '''
        return f'({self.x}, {self.y}) - {self.walls}'

    
    def construct(self) -> None:
        '''
        Draws the cells onto the pygame window. If the cell has been visited, it will be marked a different color.
        Lines will be drawn for the cell based on if the provided walls dictionary is marked true. If it is true for a given
        direction, then it will be drawn onto the screen.
        '''
        x_location = self.x * self.size
        y_location = self.y * self.size

        if self.visited:
            pygame.draw.rect(self.win, (32, 42, 68), (x_location, y_location, self.size, self.size))
        if self.walls['up']:
            pygame.draw.line(self.win, BLACK, (x_location, y_location), (x_location + self.size, y_location), 2)
        if self.walls['right']:
            pygame.draw.line(self.win, BLACK, (x_location + self.size, y_location), (x_location + self.size, y_location  + self.size), 2)
        if self.walls['down']:
            pygame.draw.line(self.win, BLACK, (x_location + self.size, y_location + self.size), (x_location, y_location  + self.size), 2)
        if self.walls['left']:
            pygame.draw.line(self.win, BLACK, (x_location, y_location + self.size), (x_location, y_location), 2)

    
    def draw_current_cell(self) -> None:
        '''
        Draws a pygame rect object that is a different color on the current cell
        '''
        x = self.x * self.size
        y = self.y * self.size

        pygame.draw.rect(self.win, (255, 224, 145), (x + 2, y + 2, self.size - 2, self.size - 2))   

    
    def x(self) -> int:
        '''
        Returns the x position of the cell

        :returns:
            int
        '''
        return self.x

    
    def y(self) -> int:
        '''
        Returns the y position of the cell

        :returns:
            int
        '''
        return self.y

    
    def size(self) -> int:
        '''
        Returns the size of the cell

        :returns:
            int
        '''
        return self.size


    def walls(self) -> dict:
        '''
        Returns the dictionary holding the directions of the cell

        :returns:
            dict
        '''
        return self.walls


    def is_visited(self) -> bool:
        '''
        Returns whether or not the cell has been visited

        :returns:
            bool
        '''
        return self.visited