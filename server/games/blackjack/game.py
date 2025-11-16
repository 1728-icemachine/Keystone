from __future__ import annotations
from typing import Any, Dict, List, Optional
import socket

from games.base import GameInterface
import globals as g


class BlackJack(GameInterface):

    def __init__(self) -> None:
        self.chips = 500
        self.cards: List[int] = []              # player’s cards
        self.dealer_cards: List[int] = []       # dealer cards
        self.betchips = 0
        self.players = []
        self.spectators = []
        self.round = 0
        self.max_rounds = 20
        self.finished = False


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

        # Create + shuffle deck if not already created globally
        g.gdeck.shuffle()

        # Dealer draws initial card
        self.dealer_cards = [g.gdeck.draw()]

        return


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
        """
        Everyone sees:
            - Dealer shows only the *first* card
            - Total cards left
        """
        return {
            "type": "bj_public_state",
            "dealer_upcard": self.dealer_cards[0] if self.dealer_cards else None,
            "deck_remaining": len(g.gdeck.cards),
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

    def card_total(self) -> int:
        total = 0
        for card in self.cards:
            val = (card % 13) + 1       # 1-13
            val = min(val, 10)          # face cards = 10
            total += val
        return total


    def dealer_total(self) -> int:
        total = 0
        for card in self.dealer_cards:
            val = (card % 13) + 1
            val = min(val, 10)
            total += val
        return total


    # --------------------------------------------------------------------
    #                             PLAYER ACTIONS
    # --------------------------------------------------------------------

    def hit(self) -> Dict[str, Any]:
        card = g.gdeck.draw()
        if card is None:
            return {"type": "bj_error", "msg": "Deck empty"}

        self.cards.append(card)
        total = self.card_total()

        busted = total > 21

        if busted:
            self.finished = True

        return {
            "type": "bj_hit_response",
            "card": card,
            "total": total,
            "busted": busted
        }


    def stand(self) -> Dict[str, Any]:
        """Dealer draws until >= 17."""
        while self.dealer_total() < 17:
            self.dealer_cards.append(g.gdeck.draw())

        self.finished = True

        return {
            "type": "bj_stand_response",
            "dealer_cards": self.dealer_cards,
            "dealer_total": self.dealer_total()
        }


    def dd(self) -> Dict[str, Any]:
        """
        Double the bet, draw 1 card, automatically stand.
        """
        if self.chips < self.betchips:
            return {"type": "bj_dd_response", "valid": False}

        # Double bet
        self.chips -= self.betchips
        self.betchips *= 2

        # Draw final card
        card = g.gdeck.draw()
        self.cards.append(card)

        # Dealer resolves immediately
        return self.stand() | {
            "type": "bj_dd_response",
            "valid": True,
            "card": card,
            "total": self.card_total(),
        }


    # --------------------------------------------------------------------
    #                               BETTING
    # --------------------------------------------------------------------

    def bet(self, betnum: int) -> Dict[str, Any]:
        valid = betnum <= self.chips

        if not valid:
            return {
                "type": "bj_bet_response",
                "valid": False,
                "remaining": self.chips,
                "can_dd": False
            }

        self.chips -= betnum
        self.betchips = betnum

        can_dd = self.chips >= betnum

        return {
            "type": "bj_bet_response",
            "valid": True,
            "remaining": self.chips,
            "can_dd": can_dd
        }
