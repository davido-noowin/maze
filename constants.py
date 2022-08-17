# constants.py
# a file that holds the constants for the maze

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# DIMENSIONS
RES = WIDTH, HEIGHT = 1202, 902
# determines how big each cell will be
# bigger number = bigger cells, and vice versa
# DEFAULTS: 100 for big cells, 20 for small cells
TILE = 20

# GRID
cols, rows = WIDTH // TILE, HEIGHT // TILE
