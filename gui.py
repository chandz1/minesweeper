import PySimpleGUI as sg
from main import Grid
from util import time_elapsed, start_clock

sg.theme("Default1")

grid = Grid(16, 16, 40)

menu_layout = [
    [
        sg.Text(
            text="{:03d}".format(grid.flags),
            font="any 24 bold",
            pad=((4, 4), (0, 0)),
            text_color="red",
            key="-FLAGS-",
        ),
        sg.Push(),
        sg.Button(border_width=2, pad=(0, 0), size=(2, 2)),
        sg.Push(),
        sg.Text(
            text="000",
            font="any 24 bold",
            pad=((4, 4), (0, 0)),
            text_color="#FB0007",
            key="-CLOCK-",
        ),
    ]
]

menu_frame = sg.Frame(
    "",
    menu_layout,
    pad=((0, 0), (0, 4)),
    expand_x=True,
    expand_y=True,
    border_width=6,
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
cells = [cell for row in grid.grid for cell in row]
for cell in cells:
    cell.bind("<Button-3>", "Right-Click")

start_time = 0
timer_active = False

while True:
    event, values = window.read(timeout=1000)

    if event == sg.WINDOW_CLOSED:
        break

    if event != "__TIMEOUT__" and not timer_active:
        timer_active = True
        start_time = start_clock()

    if timer_active:
        window["-CLOCK-"].update("{:03d}".format(time_elapsed(start_time)))

    print(event)
    if "Right-Click" in event:
        i, j = event[0]
        if grid.grid[i][j].flag_status():
            window[event[0]].update(
                text="",
                disabled=False,
            )
            grid.flags += 1
            window["-FLAGS-"].update("{:03d}".format(grid.flags))

        else:
            if grid.flags > 0:
                window[event[0]].update(
                    text="?",
                    disabled=True,
                )
                grid.flags -= 1
                window["-FLAGS-"].update("{:03d}".format(grid.flags))
            else:
                continue
        grid.grid[i][j].toggle_flag()
        continue

    if event == "__TIMEOUT__":
        continue

    i, j = event
    if not grid.grid[i][j].flagged:
        if grid.grid[i][j].is_mine():
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
