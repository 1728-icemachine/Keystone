from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Input, Button
from .tui import TicTacToe

import globals as g

def pfile(text):
    with open("DEBUG.txt", "a") as f:
        f.write(text + "\n")

class KeystoneApp(App):
    players = 0
    CSS_PATH = "main_menu.tcss"
    logged_in = False
    
    SCREENS = {
        "ttt": TicTacToe,
    }

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Main Menu", id="title"),
            Static(f"Username: {g.username}", id="user-label"),
            Input(placeholder="Enter username…", id="username-input"),
            Button("Set Username", id="set-btn"),
            Button("Connect to server", id="cts-btn"),
            Button("Play tictactoe",id="ttt")
        )


    def push_app_screen(self,screen_id):
        self.push_screen(screen_id)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "ttt":
            if g.player_type:
                if self.players < 2:
                    self.players = g.cb_pool.call("get_players")
                if self.players >= 2 and g.player_type == "host":
                    g.cb_pool.call("pick_game","ttt")
                    json_data = g.cb_pool.call("wait_for_packet")
                    send_data = {"type":"tictactoe_trigger"}
                    g.cb_pool.call("send_packet",send_data)
                    #if g.player_type == "host":
                    g.my_turn_event.set()
                    pfile("in host")
                    self.push_screen("ttt")

        if event.button.id == "set-btn":
            text = self.query_one("#username-input", Input).value
            if text.strip():
                g.username = text
                # Update the label widget
                user_label = self.query_one("#user-label", Static)
                user_label.update(f"Username: {g.username}")

        elif event.button.id == "cts-btn":
            if not self.logged_in:
                g.player_type = g.cb_pool.call("login")
                pfile(f"{g.player_type} logged in")
                self.logged_in = True
                g.cb_pool.call("start_thread")
