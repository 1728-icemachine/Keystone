from textual.app import App, ComposeResult
from textual.widgets import Static, Button
from textual import containers
import pyfiglet

class GridApp(App):
    CSS_PATH = "tic_tac_toe.tcss"
    cells = []

    def compose(self) -> ComposeResult:
        # Grid container
        with containers.Grid(id="grid"):
            for i in range(9):
                cell = Button(pyfiglet.figlet_format(""), id=f"btn{i}")
                self.cells.append(cell)
                #yield Static(f"{i}", classes="box")
                yield cell

    def set_cell(self, pos, sign):
        self.cells[pos].label = pyfiglet.figlet_format(sign)
    

    def on_button_pressed(self, event):
        pos = int(event.button.id[-1:])
        #send out to request sending thing
        #if request == success:
        #and is host:
        self.set_cell(pos, )
        

GridApp().run()

