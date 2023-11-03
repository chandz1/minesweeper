import PySimpleGUI as sg
from main import Grid

sg.theme("Default1")

grid = Grid(15, 15, 3)

menu_layout = [
    [
        sg.Text(text="000", font="any 24 bold", pad=((4, 4),(0, 0)), text_color="red"),
        sg.Push(),
        sg.Button(border_width=2, pad=(0, 0), size=(2, 2)),
        sg.Push(),
        sg.Text(text="100", font="any 24 bold", pad=((4, 4),(0, 0)), text_color="#FB0007"),
    ]
]

button_layout = [
    [sg.Button(border_width=2, pad=(0, 0)) for _ in range(grid.width)]
    for _ in range(grid.height)
]

menu_frame = sg.Frame("", menu_layout, pad=((0, 0),(0, 4)), expand_x=True, expand_y=True, border_width=6)
button_frame = sg.Frame("", button_layout, pad=((0, 0),(4, 0)), expand_x=True, expand_y=True, border_width=6)

layout = [
    [sg.VPush()],
    [menu_frame],
    [button_frame],
    [sg.VPush()],
]

window = sg.Window("Minesweeper", layout=layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

window.close()
