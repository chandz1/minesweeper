import random

# Cell class
class Cell:
    # Initialize a cell
    def __init__(self):
        self.is_mine = False
        self.flagged = False
        self.revealed = False

    # Add a mine to the cell
    def add_mine(self):
        self.is_mine = True

    # Toggle the flag state
    def toggle_flag(self):
        self.flagged = not self.flagged

    # Reveal the cell state 
    def reveal(self):
        self.revealed = True  

# Grid class
class Grid:
    # Initialize a Grid
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.add_mines()

    # Add mines to the grid at random
    def add_mines(self):
        mine_count = 0 
        while mine_count < self.mines:
            x,y = random.randint(0,self.width-1), random.randint(0,self.height-1)
            if not self.grid[x][y].is_mine:
                self.grid[x][y].add_mine()
                mine_count += 1
