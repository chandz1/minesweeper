import random
import PySimpleGUI as sg


# Cell class
class Cell(sg.Button):
    # Initialize a cell
    def __init__(self, coords, **kwargs):
        super().__init__(**kwargs)
        self.is_mine = False
        self.flagged = False
        self.revealed = False
        self.coords = coords
        self.surr_mines = 0

    # Add a mine to the cell
    def set_mine(self):
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
        self.flags = mines
        self.grid = [
            [
                Cell(
                    (i, j),
                    border_width=2,
                    font="any 16 bold",
                    size=(1, 1),
                    pad=(0, 0),
                    key=(i, j),
                    button_color="#BDBDBD",
                    disabled_button_color=("black", "#BDBDBD"),
                )
                for i in range(row)
            ]
            for j in range(column)
        ]
        self.add_mines()

    # Add mines to the grid at random
    def add_mines(self):
        mine_count = 0
        while mine_count < self.mines:
            y, x = random.randint(0, self.row - 1), random.randint(0, self.column - 1)
            if not self.grid[x][y].is_mine:
                self.grid[x][y].set_mine()
                mine_count += 1

    def calc_surr_mines(self, i, j):
        surr_mines = 0
        for a in range(i - 1, i + 2):
            for b in range(j - 1, j + 2):
                if a == i and b == j:
                    continue
                if 0 <= a < self.row and 0 <= b < self.column:
                    print(a, b)
                    if self.grid[a][b].is_mine:
                        surr_mines += 1
        self.grid[i][j].surr_mines = surr_mines
