from cgi import print_form
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
    def __init__(self, row, column, mines):
        self.row = row
        self.column = column
        self.mines = mines
        self.grid = [[Cell() for _ in range(row)] for _ in range(column)]
        self.add_mines()

    # Add mines to the grid at random
    def add_mines(self):
        mine_count = 0
        while mine_count < self.mines:
            y, x = random.randint(0, self.row - 1), random.randint(0, self.column - 1)
            if not self.grid[x][y].is_mine:
                self.grid[x][y].add_mine()
                mine_count += 1
