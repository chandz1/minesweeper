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
        self.surr_flags = 0
        self.surr_cells = []
        self.__calc_surr_cells()

    # Add a mine to the cell
    def set_mine(self):
        self.mine = True

    # Check if cell contains mine
    def is_mine(self):
        return self.mine

    # Toggle the flag state
    def toggle_flag(self, flag_count):
        if self.reveal_status:
            return flag_count
        if self.flag:
            super().update(
                text="",
                disabled=False,
            )
            self.flag = not self.flag
            return flag_count + 1
        else:
            if flag_count > 0:
                super().update(
                    text="?",
                    disabled=True,
                )
                self.flag = not self.flag
                return flag_count - 1
            else:
                return flag_count

    # Get flag status
    def flagged(self):
        return self.flag

    # Reveal the cell state
    def reveal(self, game_over=False, grid=None):
        # If the cell has a flag and the game isn't over return
        if self.reveal_status or (self.flag and not game_over):
            return
        # If game over then update false flags to red color and return
        elif self.flag and game_over and not self.mine:
            super().update(
                text="?",
                disabled=True,
                button_color="#BDBDBD",
                disabled_button_color=("red", "#BDBDBD"),
            )
            return
        # If the cell has a flag and mine then return
        elif self.flag and self.mine:
            return

        self.reveal_status = True
        grid.increment_revealed()
        if self.mine:
            super().update(
                text="💣",
                disabled=True,
                button_color="red",
                disabled_button_color=("black", "red"),
            )
            return "mine"
        elif game_over:
            super().update(text="", disabled=True)
        elif self.surr_mines:
            super().update(
                text=str(self.surr_mines),
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
            for coords in self.surr_cells:
                grid.grid[coords[0]][coords[1]].reveal(grid=grid)

    # Check if cell has been revealed
    def revealed(self):
        return self.reveal_status

    # Set surrounding mine count
    def set_surr_mines(self, mine_count):
        self.surr_mines = mine_count

    # Get surrounding mine count
    def get_surr_mines(self):
        return self.surr_mines

    # Calculate and set surrouding cells based on grid row and column
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

    # Set surrounding flags count
    def set_surr_flags(self, flag_count):
        self.surr_flags = flag_count

    # Get surrounding flag count
    def get_surr_flags(self):
        return self.surr_flags


# Grid class
class Grid:
    # Initialize a Grid
    def __init__(self, row=16, column=16, total_mines=40):
        self.row = row
        self.column = column
        self.size = row * column
        self.total_mines = total_mines
        self.revealed = 0
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
            y, x = random.randint(0, self.row - 1), random.randint(
                0, self.column - 1
            )
            if not self.grid[x][y].is_mine():
                self.grid[x][y].set_mine()
                mine_count += 1

    def calc_surr_mines(self, cell):
        surr_mines = 0
        for a, b in cell.get_surr_cells():
            if self.grid[a][b].is_mine():
                surr_mines += 1
        cell.set_surr_mines(surr_mines)

    def calc_surr_flags(self, cell):
        surr_flags = 0
        for a, b in cell.get_surr_cells():
            if self.grid[a][b].flagged():
                surr_flags += 1
        cell.set_surr_flags(surr_flags)

    def reveal_surr(self, cell):
        for a, b in cell.get_surr_cells():
            temp_cell = self.grid[a][b]
            if temp_cell.is_mine():
                if temp_cell.reveal(grid=self) == "mine":
                    return "mine"
        for a, b in cell.get_surr_cells():
            self.grid[a][b].reveal(grid=self)
        return

    def increment_revealed(self):
        self.revealed += 1

    def get_revealed(self):
        return self.revealed
