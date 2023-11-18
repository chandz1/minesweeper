import random
import PySimpleGUI as sg


# Cell class
class Cell(sg.Button):
    # Initialize a cell
    def __init__(self, coords, **kwargs):
        super().__init__(**kwargs)
        self.coords = coords
        self.mine = False
        self.flag = False
        self.revealed = False
        self.surr_mines = 0

    # Add a mine to the cell
    def set_mine(self):
        self.mine = True

    # Check if cell contains mine
    def is_mine(self):
        return self.mine

    # Toggle the flag state
    def toggle_flag(self):
        self.flag = not self.flag

    # Get flag status
    def flagged(self):
        return self.flag

    # Reveal the cell state
    def reveal(self):
        self.revealed = True

    # Increment surr mine count
    def set_surr_mines(self, mine_count):
        self.surr_mines = mine_count


# Grid class
class Grid:
    # Initialize a Grid
    def __init__(self, row, column, total_mines):
        self.row = row
        self.column = column
        self.total_mines = total_mines
        self.flags = total_mines
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
        self.__add_mines()

    # Add mines to the grid at random
    def __add_mines(self):
        mine_count = 0
        while mine_count < self.total_mines:
            print(mine_count)
            y, x = random.randint(0, self.row - 1), random.randint(
                0, self.column - 1
            )
            if not self.grid[x][y].is_mine():
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
                    if self.grid[a][b].is_mine():
                        surr_mines += 1
        self.grid[i][j].set_surr_mines(surr_mines)
