from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

from core.GameManager import GameManager
import globals as g
import json
import socket
from games.blackjack import game
class BlackJackManager(GameManager):

    def __init__(self):
        return

    def play_game(self,client_socket) -> None:
        bjgame = game.BlackJack()
        bjgame.init()
        self.send_bet_screen(client_socket)
        while True:
            data = client_socket.recv(1024)
            if not data:continue
            try:
                if ()
                packet = json.loads(data.decode())
                bjgame.handle_action(client_socket,packet)


            except json.JSONDecodeError:
                break

    
    def handle_player_action(self, player_id: socket.socket, action: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Handles player input"""
        pass

    
    def get_public_state(self) -> Dict[str, Any]:
        """Information visible to all players"""
        pass

    
    def get_private_state(self, player_id: socket.socket) -> Dict[str, Any]:
        """Private info specific to one player"""
        pass

    
    def end_game(self) -> Dict[str, Any]:
        """End game, triggered by condition or external event"""
        pass
    def send_game_state(self,client_socket):

        packet = {"type" : "ttt_state_update", "state": g.game.get_public_state()}
        print(f"in the game state")
        json_data = json.dumps(packet).encode("utf-8")
        client_socket.sendall(json_data)
