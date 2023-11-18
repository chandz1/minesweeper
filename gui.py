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
    cell.bind("<Button-1>", "Left-Click")
    cell.bind("<Button-2>", "Middle-Click")
    cell.bind("<Button-3>", "Right-Click")

start_time = 0
timer_active = False


def on_right_click(event):
    i, j = event[0]
    cell = grid.grid[i][j]
    if event[1] == "Right-Click":
        if cell.flagged():
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
                return
        cell.toggle_flag()


def on_left_middle_click(event):
    i, j = event[0]
    cell = grid.grid[i][j]
    if event[1] == "Left-Click" or event[1] == "Middle-Click":
        if not cell.flagged():
            if cell.is_mine():
                cell.reveal()
                return "mine"
            grid.calc_surr_mines(i, j)
            if cell.surr_mines == 0:
                window[event[0]].update(
                    text="",
                    disabled=True,
                    button_color="gray",
                )
                window[event[0]].unbind("<Button-3>")
                return

            window[event[0]].update(
                str(cell.surr_mines),
                disabled=True,
                button_color="gray",
                disabled_button_color=("black", "gray"),
            )
            window[event[0]].unbind("<Button-3>")


while True:
    event, values = window.read(timeout=1000)

    if event == sg.WINDOW_CLOSED:
        break

    if event == "__TIMEOUT__" and not timer_active:
        continue
    elif not timer_active:
        timer_active = True
        start_time = start_clock()
    elif timer_active:
        window["-CLOCK-"].update("{:03d}".format(time_elapsed(start_time)))
        if event == "__TIMEOUT__":
            continue

    print(event)

    match event[1]:
        case "Right-Click":
            on_right_click(event)
        case "Left-Click" | "Middle-Click":
            if on_left_middle_click(event) == "mine":
                continue
            else:
                continue

window.close()
