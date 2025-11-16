import socket
import threading
import json
import globals as g
from games.tictactoe import tictactoe
from games.tictactoe import game as tttgame
from games.blackjack import blackjack
IP_ADDRESS = "192.168.0.233"
PORT = 8080

def num_players(client_socket):
    print(len(g.players))
    packet = {"type": "numplayers_answer", "num": len(g.players)}
    json_data = json.dumps(packet).encode("utf-8")
    client_socket.sendall(json_data)

def load_tic():
    ttt_game = tttgame.TicTacToe()
    g.game = ttt_game
    g.game.init()
    for x in range(len(g.players)):
        role = "spectator"
        if x == 0: role = "X" 
        elif x == 1: role = "O"
        packet = {"type": "tictactoe_confirm", "role":role  }
        json_data = json.dumps(packet).encode("utf-8")
        g.players[x].sendall(json_data)
        ttt = tictactoe.TicTacToeManager()
        ttt.play_game(g.players[x])
    
def load_black(client_socket):
    for x in range (len(g.players)):
        packet = {"type": "blackjack_confirm"}
        json_data = json.dumps(packet).encode("utf-8")
        g.players[x].sendall(json_data)
        bj = blackjack.BlackJackManager()
        bj.play_game(g.players[x])

def error_packet(client_socket):
    packet = {"type": "error"}
    json_data = json.dumps(packet).encode("utf-8")
    client_socket.sendall(json_data)

def login_player(client_socket):

    if g.players[0] != client_socket:
        pt = "player"
    else:
        pt = "host"
    packet = {"type": "login_confirm", "player_type": pt}
    json_data = json.dumps(packet).encode("utf-8")
    client_socket.sendall(json_data)

def confirm_packet(client_socket):
    packet = {"type": "confirm", "accepted": True}
    json_data = json.dumps(packet).encode("utf-8")
    client_socket.sendall(json_data)

def on_new_client(client_socket, client_address):
    print(f"Client connected: {client_address[0]}:{client_address[1]}")
    try:
        confirm_packet(client_socket)
        g.players.append(client_socket)
        while True:
            data = client_socket.recv(1024)
            if not data: continue
            try:
                packet = json.loads(data.decode())
                if packet["type"] == "login":
                    login_player(client_socket)
                    g.players_user[client_socket] = packet["name"]
                elif packet["type"] =="numplayers":
                    num_players(client_socket)
                elif packet ["type"] == "tictactoe_start":
                    load_tic()
                elif packet ["type"] == "blackjack_start":
                    load_black(client_socket)
                else:
                    error_packet(client_socket)
            except json.JSONDecodeError:
                break
    except ConnectionAbortedError:
        print(f"Client disconnected: {client_address[0]}:{client_address[1]}")
    finally:
        g.players.remove(client_socket)
        del g.players_user[client_socket]
        client_socket.close()



def start_server(host, port):
    g.init_vars()
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to a specific host and port
    server_socket.bind((host, port))
        # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server started. Listening on {host}:{port}")
    while True:
    # Accept a client connection
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(
            target=on_new_client,
            args=(client_socket, client_address),
            daemon=True
        )
        client_thread.start()# Start the server
start_server('0.0.0.0', 8080)