from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Input, Button
from .tui import TicTacToe
from networking.client import login

import globals as g

class MyApp(App):
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
            login()
            self.push_screen("ttt")
