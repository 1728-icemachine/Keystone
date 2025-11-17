from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual import containers
import pyfiglet
import globals as g

def pfile(text):
    with open("DEBUG.txt", "a") as f:
        f.write(text + "\n")

class TicTacToe(Screen):
    CSS_PATH = "ttt.tcss"
    cells = []
    my_turn = True

    def compose(self):
        pfile(f"composing {g.player_type}'s ttt")
        # Grid container
        if not g.player_type == "host":
            self.my_turn = False
        with containers.Grid(id="grid"):
            for i in range(9):
                cell = Button(pyfiglet.figlet_format(""), id=f"btn{i}")
                self.cells.append(cell)
                yield cell

    def update_board(self,board):
        flat_board = [item for sublist in board for item in sublist]
        for i in range(9):
            self.cells[i].label = flat_baord[i]
        self.my_turn = True

    def set_cell(self, pos):
        sign = "X"
        if g.player_type == "player":
            sign = "O"
        self.cells[pos].label = pyfiglet.figlet_format(sign)

    def on_button_pressed(self, event):
        if self.my_turn:
            pos = int(event.button.id[-1:])
            if g.cb_pool.call("click_cell",(pos % 3, pos//3)) != 0:
                self.set_cell(pos)
                self.my_turn = False
                g.my_turn_event.set()
            else:
                print("fucky wucky")
