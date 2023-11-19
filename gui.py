import PySimpleGUI as sg
from main import Grid
from util import time_elapsed, start_clock

sg.theme("Default1")

grid = Grid()

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
        sg.Button(
            image_source="smiley.png",
            image_size=(30, 30),
            border_width=2,
            pad=(0, 0),
            size=(2, 2),
            key="-RESET-",
        ),
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
    key="-GRID-",
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


def reset_game(grid):
    del grid
    grid = Grid()


def end_game():
    for cell in cells:
        cell.unbind("<Button-1>")
        cell.unbind("<Button-2>")
        cell.unbind("<Button-3>")
        cell.reveal(game_over=True)


def on_right_click(coords):
    cell = grid.grid[coords[0]][coords[1]]
    grid.flags = cell.toggle_flag(grid.flags)
    window["-FLAGS-"].update("{:03d}".format(grid.flags))


def on_left_middle_click(coords):
    cell = grid.grid[coords[0]][coords[1]]
    grid.calc_surr_mines(cell)
    if cell.reveal() == "mine":
        end_game()


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
    if event == "-RESET-":
        reset_game(grid)

    match event[1]:
        case "Right-Click":
            on_right_click(event[0])
        case "Left-Click" | "Middle-Click":
            if on_left_middle_click(event[0]) == "mine":
                continue
            else:
                continue

window.close()
