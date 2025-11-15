from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple

from games.base import GameInterface

class TicTacToe(GameInterface):
    """
    Tic-Tac-Toe game logic
    
    Roles:
        - "X" and "O" are players
        - Any extra players are spectators
    """
    
    BOARD_SIZE = 3
    
    def __init__(self) -> None:
        self.board: List[List[str]] = [
            ["" for _ in range(self.BOARD_SIZE)
            for _ in range(self.BOARD_SIZE)]
        ]
        
        # role -> player_id
        self.players: Dict[str, Optional[str]] = {"X": None, "O": None}
        self.spectators: List[str] = []
        self.turn: str = "X"
        self.status: str = "playing" # "playing" | "win" | "draw"
        self.winner_role: Optional[str] = None
        self.winning_line: Optional[List[Tuple[int, int]]] = None
        
    @property
    def name(self) -> str:
        return "tictactoe"
    
    def init(self, players: List[str], config: Optional[Dict[str, Any]] = None) -> None:
        """
        Assign first two players to X/O in order.
        Rest of the players are spectators
        """
        self.reset_board()
        
        if players:
            self.players["X"] = players[0]
        if len(players) > 1:
            self.players["O"] = players[1]
        if len(players) > 2:
            self.spectators = players[2:]
        else:
            self.spectators = []
        
        self.turn = "X"
        self.status = "playing"
        self.winner_role = None
        self.winning_line = None
        
    def handle_action(self, player_id: str, action: Dict[str, Any]):
        """
        Check notion for expected format
        """
        
        # Checks
        if self.status != "playing":
            return False, "Game is already over"
        
        role = self.role_for_player(player_id)
        if role is None:
            return False, "Spectators can't make moves"
        
        if role != self.turn:
            return False, "It is not your turn"
        
        if action.get("action") != "place":
            return False, f"Unknown action: {action.get(self.turn)}"
        
        try:
            row = int(action["row"])
            col = int(action["col"])
        except (KeyError, ValueError, TypeError):
            return False, "Invalid row/col"
        
        if not self.in_bounds(row, col):
            return False, "Move out of bounds"

        if self.board[row][col] != "":
            return False, "Cell is already taken"
        
        # Move
        self.board[row][col] = role
        
        # Game status
        if self.check_win(role):
            self.status = "win"
            self.winner_role = role
        elif self.is_board_full():
            self.status = "draw"
        else:
            self.turn = "O" if self.turn == "X" else "X"
        
        return True, None
    
    def get_public_state(self) -> Dict[str, Any]:
        """
        Returns public game state
        
        """
        return {
            "board": self._copy_board(),
            "turn": self._turn,
            "status": self._status,
            "winner_role": self._winner_role,
            "winning_line": self._winning_line,
            "players": {
                "X": self._players["X"],
                "O": self._players["O"],
            },
            "spectators": list(self._spectators),
        }
        
    def get_private_state(self, player_id: str) -> Dict[str, Any]:
        """
        Tic-Tac-Toe has not private info
        """
        return {}
    
    def is_over(self) -> bool:
        return self.status in ("win", "draw")
    
    def result(self) -> Dict[str, Any]:
        """
        This is the game end packet
        """
        winner_id = None
        if self._winner_role is not None:
            winner_id = self._players.get(self._winner_role)

        return {
            "status": self._status,
            "winner_role": self._winner_role,
            "winner_player_id": winner_id,
            "winning_line": self._winning_line,
        }
    
    # Helper Functions
    
    def reset_board(self) -> None:
        self.board = [
            ["" for _ in range(self.BOARD_SIZE)
            for _ in range(self.BOARD_SIZE)]
        ]
    
    def role_for_player(self, player_id: str) -> Optional[str]:
        for role, pid in self.players.items():
            if pid == player_id:
                return role
        return None
    
    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row <= self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE
    
    def is_board_full(self) -> bool:
        return all(cell != "" for row in self.board for cell in row)
    
    def copy_board(self) -> List[List[str]]:
        return [row[:] for row in self.board]
    
    def check_win(self, role: str) -> bool:
        lines : List[List[Tuple[int, int]]] = []
        
        for r in range(self.BOARD_SIZE):
            lines.append([r, c] for c in range(self.BOARD_SIZE))
            
        for c in range(self.BOARD_SIZE):
            lines.append([r, c] for r in range(self.BOARD_SIZE))
        
        # Diagonal Lines
        lines.append([i, i] for i in range(self.BOARD_SIZE))
        lines.append([(i, self.BOARD_SIZE - 1 - i) for i in range(self.BOARD_SIZE)])
        
        for line in lines:
            if all(self.board[r][c] == role for r,c in line):
                self.winning_line = line
                return True
        self.winning_line = None
        return False