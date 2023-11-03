import PySimpleGUI as sg
from main import *

sg.theme("Default1")

grid = Grid(16, 16, 40)

menu_layout = [
    [
        sg.Text(text="000", font="any 24 bold", pad=((4, 4), (0, 0)), text_color="red"),
        sg.Push(),
        sg.Button(border_width=2, pad=(0, 0), size=(2, 2)),
        sg.Push(),
        sg.Text(
            text="100", font="any 24 bold", pad=((4, 4), (0, 0)), text_color="#FB0007"
        ),
    ]
]

menu_frame = sg.Frame(
    "", menu_layout, pad=((0, 0), (0, 4)), expand_x=True, expand_y=True, border_width=6
)

button_frame = sg.Frame(
    "",
    grid.grid,
    pad=((0, 0), (4, 0)),
    expand_x=True,
    expand_y=True,
    border_width=6,
)

layout = [
    [sg.VPush()],
    [menu_frame],
    [button_frame],
    [sg.VPush()],
]

window = sg.Window("Minesweeper", layout=layout, finalize=True)
buttons_1d = [button for row in grid.grid for button in row]
for btn in buttons_1d:
    btn.bind("<Button-3>", "Right-Click")


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    print(event)
    if "Right-Click" in event:
        i, j = event[0]
        if grid.grid[i][j].flagged:
            window[event[0]].update(
                "",
                disabled=False,
            )
        else:
            window[event[0]].update(
                "?",
                disabled=True,
            )
        grid.grid[i][j].toggle_flag()
        continue

    i, j = event
    if not grid.grid[i][j].flagged:
        if grid.grid[i][j].is_mine:
            break
        grid.calc_surr_mines(i, j)
        if grid.grid[i][j].surr_mines == 0:
            window[event].update("", disabled=True, button_color="gray")
            window[event].unbind("<Button-3>")

            continue

        window[event].update(
            str(grid.grid[i][j].surr_mines),
            disabled=True,
            button_color="gray",
            disabled_button_color=("black", "gray"),
        )
        window[event].unbind("<Button-3>")

window.close()
