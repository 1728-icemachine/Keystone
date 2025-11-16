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

    def update_board(self,board):
        flat_board = [item for sublist in board for item in sublist]
        for i in range(9):
            self.cells[i].label = flat_baord[i]

    def set_cell(self, pos):
        sign = "X"
        if g.player_type == "player":
            sign = "O"
        self.cells[pos].label = pyfiglet.figlet_format(sign)

    def on_button_pressed(self, event):
        pos = int(event.button.id[-1:])
        if g.cb_pool.call("click_cell",(pos % 3, pos//3)) != 0:
            self.set_cell(pos)
            g.my_turn_event.set()
        else:
            print("fucky wucky")
