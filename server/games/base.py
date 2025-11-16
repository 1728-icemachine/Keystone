from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import socket

class GameInterface(ABC):
    """
    Game Interface that all games should implement
    
    Purely Game logic and state
    """
    
    @abstractmethod
    def init(self, config: Optional[Dict[str, Any]] = None) -> None:
        '''
        Initializes a new game
        
        Args:
            Fill out eventually...
        '''
        ...
        
    @abstractmethod
    def handle_action(self, player_id: socket.socket, action: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Apply an action sent by a player
        
        Returns:
            bool is true indicates success otherwise if bool is false there was an error,
            in which case the optional string is populated with the error message
        
        Args:
            Fill this out eventually...
        """
        ...
    
    @abstractmethod
    def get_public_state(self) -> Dict[str, Any]:
        """
        State visible to everyone
        ! Make sure this is serializable to JSON
        """
        ...
    
    
    @abstractmethod
    def get_private_state(self, player_id: socket.socket) -> Dict[str, Any]:
        """
        State visible to a specific player
        For games with no private info, return {}
        
        Args:
            Fill this out eventually...
        """
        ...
    
    @abstractmethod
    def is_over(self) -> bool:
        """
        Returns True if the game has ended
        """
        ...
    
    @abstractmethod
    def results(self) -> Dict[str, Any]:
        """
        Final Result of the game
        """
        ...
        
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Name used by GameManager & UI
        ex. "tictactoe"
        """
        ...