import PySimpleGUI as sg
from main import Cell
from main import Grid

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

button_layout = [
    [sg.Button(border_width=2, size=(1,1), pad=(0, 0), key=(i,j), button_color="#BDBDBD") for i in range(grid.column)]
    for j in range(grid.row)
]

menu_frame = sg.Frame(
    "", menu_layout, pad=((0, 0), (0, 4)), expand_x=True, expand_y=True, border_width=6
)
button_frame = sg.Frame(
    "",
    button_layout,
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

window = sg.Window("Minesweeper", layout=layout)

while True:
    event, values = window.read()
    i, j = event
    if grid.grid[i][j].is_mine:
        break
    else:
        grid.calc_surr_mines(i,j)
        if grid.grid[i][j].surr_mines == 0:
            window[event].update(disabled=True, button_color = "gray")
            continue
        window[event].update(str(grid.grid[i][j].surr_mines))
        window[event].update(disabled=True, button_color="gray", disabled_button_color = ("blue", "gray"))
    if event == sg.WINDOW_CLOSED:
        break

window.close()
