import PySimpleGUI as gui
from main import Grid

gui.theme('DarkGrey13')

size = (1280, 720)

grid = Grid(10,10,3)
layout = [[gui.Button() for _ in range(grid.width)] for _ in range(grid.height)]

window = gui.Window('Minesweeper', layout=layout, size=size)

while True:
    event, values = window.read()
    
    if event == gui.WINDOW_CLOSED:
        break

window.close()
