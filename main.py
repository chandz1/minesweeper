import random
import PySimpleGUI as sg


# Cell class
class Cell(sg.Button):
    # Initialize a cell
    def __init__(self, coords, row, column, **kwargs):
        super().__init__(**kwargs)
        self.coords = coords
        self.max_row = row
        self.max_column = column
        self.mine = False
        self.flag = False
        self.reveal_status = False
        self.surr_mines = 0
        self.surr_cells = []
        self.__calc_surr_cells()

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
        if self.reveal_status or self.flag:
            return
        self.reveal_status = True
        if self.mine:
            super().update(text="💣", disabled=True)
            return "mine"
        elif self.surr_mines:
            super().update(
                str(self.surr_mines),
                disabled=True,
                button_color="gray",
                disabled_button_color=("black", "gray"),
            )
        else:
            super().update(
                text="",
                disabled=True,
                button_color="gray",
            )

    # Check if cell has been revealed
    def revealed(self):
        return self.reveal_status

    # Increment surr mine count
    def set_surr_mines(self, mine_count):
        self.surr_mines = mine_count

    # Set surrouding cells based on grid row and column
    def __calc_surr_cells(self):
        i, j = self.coords
        for a in range(i - 1, i + 2):
            for b in range(j - 1, j + 2):
                if a == i and b == j:
                    continue
                if 0 <= a < self.max_row and 0 <= b < self.max_column:
                    self.surr_cells.append((a, b))

    # Get surrouding cells array
    def get_surr_cells(self):
        return self.surr_cells


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
                    row,
                    column,
                    border_width=2,
                    font="any 16 bold",
                    size=(1, 1),
                    pad=(0, 0),
                    key=(i, j),
                    button_color="#BDBDBD",
                    disabled_button_color=("black", "#BDBDBD"),
                )
                for j in range(column)
            ]
            for i in range(row)
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
                    if self.grid[a][b].is_mine():
                        surr_mines += 1
        self.grid[i][j].set_surr_mines(surr_mines)
