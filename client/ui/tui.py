from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual import containers
import pyfiglet
import globals as g

class TicTacToe(Screen):
    CSS_PATH = "ttt.tcss"
    cells = []

    def compose(self):
        # Grid container
        with containers.Grid(id="grid"):
            for i in range(9):
                cell = Button(pyfiglet.figlet_format(""), id=f"btn{i}")
                self.cells.append(cell)
                yield cell

    def set_cell(self, pos, sign):
        self.cells[pos].label = pyfiglet.figlet_format(sign)
    

    def on_button_pressed(self, event):
        pos = int(event.button.id[-1:])
        if g.call(click_callback((pos % 3, pos//3)) != -1:
            self.set_cell(pos,"O" )
        else:
            print("fucky wucky")
