from __future__ import annotations
from typing import Any, Dict, List, Optional
import socket

from games.base import GameInterface
import globals as g


class BlackJack(GameInterface):

    def __init__(self) -> None:
        self.chips = 500
        self.cards: List[int] = []              # player’s cards
        self.betchips = 0
        self.players = []
        self.spectators = []
        self.round = 0
        self.max_rounds = 20
        self.finished = False
        self.pname: socket.socket
        self.playernum = -1
        self.can_dd = False
        self.my_turn = False

    @property
    def name(self) -> str:
        return "blackjack"
    

    def init(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize players from g.players, separating spectators if > 7.
        Shuffle global deck BEFORE playing.
        """
        if len(g.players) <= 7:
            self.players = g.players
        else:
            self.players = g.players[:7]
            self.spectators = g.players[7:]

        return

    def init_name(self,player_id: socket.socket):
        self.name = socket.socket
        if self.name in self.players:
            self.playernum = self.players.index(self.name)

    def getpnum(self):
        return self.playernum
    def makego(self):
        self.my_turn = True
    # --------------------------------------------------------------------
    #                             ACTION HANDLING
    # --------------------------------------------------------------------
    
    
    def handle_action(self, player_id: socket.socket, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatch table for blackjack player actions.
        """
        atype = action.get("type")

        if atype == "bj_bet":
            return self.bet(action["amount"])

        elif atype == "bj_action":
            move = action.get("move")

            if move == "hit":
                return self.hit()

            elif move == "stand":
                return self.stand()

            elif move == "dd":
                return self.dd()

        return {"type": "error", "msg": "Unknown blackjack action"}


    # --------------------------------------------------------------------
    #                              GAME STATE
    # --------------------------------------------------------------------

    def get_public_state(self) -> Dict[str, Any]:
        return {
            "type": "bj_public_state",
            "dealer_cards": g.dcards if g.dcards else None,
            "deck_remaining": len(g.gdeck),
            "round": self.round,
            "max_rounds": self.max_rounds,
        }


    def get_private_state(self, player_id: socket.socket) -> Dict[str, Any]:
        """
        Player sees:
            - Their own cards
            - Their chip count
            - Their current bet
        """
        return {
            "type": "bj_private_state",
            "hand": self.cards,
            "total": self.card_total(),
            "chips": self.chips,
            "bet": self.betchips,
            "done": self.finished,
            "my_turn": self.myturn,

        }


    def is_over(self) -> bool:
        return self.finished


    def results(self) -> Dict[str, Any]:
        """
        Very simple results:
            - Compare player total vs dealer
        """
        p = self.card_total()
        d = self.dealer_total()

        if p > 21:
            msg = "player_bust"
        elif d > 21 or p > d:
            msg = "player_win"
        elif p == d:
            msg = "push"
        else:
            msg = "dealer_win"

        self.finished = True

        return {
            "type": "bj_results",
            "result": msg,
            "player_total": p,
            "dealer_total": d,
        }


    # --------------------------------------------------------------------
    #                             GAME LOGIC
    # --------------------------------------------------------------------

    def card_total(self):
        ranks = [(c % 13) for c in self.cards]

        total = 0
        aces = 0

        for r in ranks:
            if r == 0:           # Ace
                aces += 1
                total += 11      # count Ace high for now
            elif r >= 10:        # J/Q/K
                total += 10
            else:
                total += (r + 1) # cards 2–10

        # If we're busting, convert Aces from 11 → 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total



    def dealer_total(self) -> int:
        total = 0
        for card in g.dcards:
            val = (card % 13) + 1
            val = min(val, 10)
            total += val
        return total


    # --------------------------------------------------------------------
    #                             PLAYER ACTIONS
    # --------------------------------------------------------------------

def hit(self):
    card = g.gdeck.draw()
    if card is None:
        return
    self.cards.append(card)
    tot = self.card_total()
    busted = tot > 21
    if busted:
        self.finished =True

def dd(self):
    """
    Double the bet, draw 1 card, automatically stand.
    """
    if self.chips < self.betchips:
        return

    # Double bet
    self.chips -= self.betchips
    self.betchips *= 2
    self.hit()


    # --------------------------------------------------------------------
    #                               BETTING
    # --------------------------------------------------------------------

def bet(self, betnum: int):
    valid = betnum <= self.chips
    if not valid:
        return
    self.chips -= betnum
    self.betchips = betnum

    self.can_dd = self.chips >= betnum
    g.numdone+=1

