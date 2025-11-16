from games import base
from games.blackjack import deck

def init_vars():
    global players
    players = []
    global players_user
    players_user = {}
    global game
    global gdeck
    gdeck = deck.Deck()

    global dcards
    dcards = []