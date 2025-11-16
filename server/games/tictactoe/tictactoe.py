from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

from core.GameManager import GameManager
import globals as g
import json
game = g.game

class TicTacToeManager(GameManager):

    def play_game(self,client_socket) -> None:
        self.send_game_state(client_socket)
        while True:
            data = client_socket.recv(1024)
            if not data:continue
            try:
                packet = json.loads(data.decode())
                if packet["type"] == "ttt_action":
                    ret = game.handle_action(packet,client_socket)
                    retpacket = []
                    retpacket["type"] = "ttt_invalid_move"
                    retpacket["valid"] = ret[0]
                    retpacket["message"] = ret[1]
                    json_data = json.dumps(retpacket).encode("utf-8")
                    client_socket.sendall(json_data)
                    if ret[0]:
                        for x in len(g.players):
                            self.send_game_state(g.players[x])
                    if (game.is_over()):
                        for x in len(g.players):
                            packet = {"type": "ttt_result", "result": game.result()}
                            json_data = json.dumps(packet).encode("utf-8")
                            g.players[x].sendall(json_data)
                    
            except json.JSONDecodeError:
                break
    def send_game_state(client_socket):

        packet = {"type" : "ttt_state_update", "state": game.get_public_state()}
        json_data = json.dumps(packet).encode("utf-8")
        client_socket.sendall(json_data)
