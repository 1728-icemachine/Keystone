from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import socket


class GameManager(ABC):

    @abstractmethod
    def play_game(self,client_socket: socket.socket) -> None:
        """Initializes a game environment"""
        pass

    @abstractmethod
    def handle_player_action(self, player_id: socket.socket, action: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Handles player input"""
        pass

    @abstractmethod
    def get_public_state(self) -> Dict[str, Any]:
        """Information visible to all players"""
        pass

    @abstractmethod
    def get_private_state(self, player_id: socket.socket) -> Dict[str, Any]:
        """Private info specific to one player"""
        pass

    @abstractmethod
    def end_game(self) -> Dict[str, Any]:
        """End game, triggered by condition or external event"""
        pass
