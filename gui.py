import PySimpleGUI as sg
from main import Grid
import time

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
            key="-TIMER-",
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
buttons_1d = [button for row in grid.grid for button in row]
for btn in buttons_1d:
    btn.bind("<Button-3>", "Right-Click")

timer_started = False
current_time = 0


while True:
    event, values = window.read(timeout=1000)

    if event == sg.WINDOW_CLOSED:
        break

    if event != "__TIMEOUT__" and not timer_started:
        timer_started = True
        real_time = time.monotonic()

    if timer_started:
        current_time = int(time.monotonic() - real_time)
        window["-TIMER-"].update("{:03d}".format(current_time))

    print(event)
    if "Right-Click" in event:
        i, j = event[0]
        if grid.grid[i][j].flagged:
            window[event[0]].update(
                "",
                disabled=False,
            )
            grid.flags += 1
            window["-FLAGS-"].update("{:03d}".format(grid.flags))

        else:
            if grid.flags > 0:
                window[event[0]].update(
                    "?",
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
