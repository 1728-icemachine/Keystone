# from textual import on
from textual.app import App
from textual.widgets import Button, Static
from textual.containers import Grid
import pyfiglet


x_ascii =""" 
\\   /\n
 \\ /\n
  X\n
 / \\\n
/   \\
"""

o_ascii = """
/‾‾\\\n
|    |\n
|    |\n
|    |\n
 \\__/
"""

cell_pos = [(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(2,0),(2,1),(2,2)]
class EventsApp(App):
    CSS_PATH = "tic_tac_toe.tcss"
    presses_count = 0
    double_border = False
    cells = [[None,None,None]]*3
    ttt_widget = None
    grid = None

    def compose(self):
        self.grid = Grid()
        i = 0
        self.grid.styles.grid_size_rows = rows = 3
        self.grid.styles.grid_size_columns = cols = 3
        self.ttt_widget = Static(id="ttt_widget")
        self.ttt_widget.styles.width = 30
        self.ttt_widget.styles.height = 30
        
        with self.grid:
            for row in range(rows):
                for col in range(cols):
                    cell = Static(pyfiglet.figlet_format("X"), id=f"btn{i}")
                    cell.styles.width = "1fr"
                    #cell.styles.width = 15
                    #cell.styles.height = 9
                    cell.styles.height = "1fr"
                    cell.styles.border = ("solid","green")
                    #cell.styles.background = "black"
                    #cell.styles.text_align = "center"
                    i += 1
                    yield cell
        yield self.ttt_widget


    def on_mount(self, text):
        self.ttt_widget.mount(self.grid)


    def on_button_pressed(self, event):
        print("HELP E") 
if __name__ == "__main__":
    app = EventsApp()
    app.run()
