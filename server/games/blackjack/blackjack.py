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
        g.gdeck.shuffle()
        bjgame.init()
        bjgame.init_name(client_socket)
        while True:
            if (g.numdone) == min(len(g.players),7) and bjgame.getpnum() ==0:
                g.numdone = 0
                bjgame.makego()

            data = client_socket.recv(1024)
            if not data:continue
            try:
                packet = json.loads(data.decode())
                bjgame.handle_action(client_socket,packet)
                for s in g.players:
                    self.send_public_state(s)
                self.send_private_state(client_socket)


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
