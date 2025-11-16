import random
from typing import List, Optional

class Deck:
    def __init__(self):
        self.cards: List[int] = list(range(52))  # 0–51

    def shuffle(self) -> None:
        random.shuffle(self.cards)
    def reset_deck(self) -> None:
        self.cards: List[int] = list(range(52))

    def draw(self) -> Optional[int]:
        if not self.cards:
            return None  # deck empty
        return self.cards.pop()  # removes and returns top card
