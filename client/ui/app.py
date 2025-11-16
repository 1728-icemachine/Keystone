from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Input, Button
from .tui import TicTacToe
import globals as g

class KeystoneApp(App):
    players = 0
    logged_in = False
    CSS_PATH = "main_menu.tcss"
    
    SCREENS = {
        "ttt": TicTacToe,
    }

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Main Menu", id="title"),
            Static(f"Username: {g.username}", id="user-label"),
            Input(placeholder="Enter username…", id="username-input"),
            Button("Set Username", id="set-btn"),
            Button("Connect to server", id="cts-btn")
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "set-btn":
            text = self.query_one("#username-input", Input).value
            if text.strip():
                g.username = text
                # Update the label widget
                user_label = self.query_one("#user-label", Static)
                user_label.update(f"Username: {g.username}")

        elif event.button.id == "cts-btn":
            if not self.logged_in:
                self.logged_in = g.cb_pool.call("login")
            if self.logged_in:
                if self.players < 2:
                    self.players = g.cb_pool.call("get_players")
                if self.players >= 2:
                    g.cb_pool.call("start_thread")
                    self.push_screen("ttt")
