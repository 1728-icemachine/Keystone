import socket
import json

IP_ADDRESS = "192.168.0.233"
PORT = 8080
USERNAME = "cole"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connects, logs in, waits for type assignment
def login():
    sock.connect((IP_ADDRESS, PORT))
    
    while True:
        data = sock.recv(1024)
        if not data:
            continue
        
        json_str = data.decode('utf-8')
        json_data = json.loads(json_str)
        print(f"Connected: {json_data['accepted']}")

        packet = {"type": "login", "name": USERNAME}
        json_data = json.dumps(packet).encode('utf-8')
        sock.sendall(json_data)
        break

    while True:
        data = sock.recv(1024)
        if not data:
            continue
        json_str = data.decode('utf-8')
        json_data = json.loads(json_str)
        return json_data['player_type']

# get number of connected players, waits for answer
def get_players():
    packet = {"type": "numplayers"}
    json_data = json.dumps(packet).encode('utf-8')
    sock.sendall(json_data)

    while True:
        data = sock.recv(1024)
        if not data:
            continue
        json_str = data.decode('utf-8')
        json_data = json.loads(json_str)
        return json_data['num']

# main loop
if __name__ == "__main__":
    player_type = login()
    print(f"Player type: {player_type}")
    choice = "ttt"
    if get_players() == 2:
        if choice == "ttt":
            type = "tictactoe_start"
            packet = {"type": type}
            json_data = json.dumps(packet).encode('utf-8')
            sock.sendall(json_data)
            
            while True:
                data = sock.recv(1024)
                if not data:
                    continue
                json_str = data.decode('utf-8')
                json_data = json.loads(json_str)
                print(json_data)
                break
        elif choice == "bj":
            type = "blackjack_start"
            packet = {"type": type}
            json_data = json.dumps(packet).encode('utf-8')
            sock.sendall(json_data)
            
            while True:
                data = sock.recv(1024)
                if not data:
                    continue
                json_str = data.decode('utf-8')
                json_data = json.loads(json_str)
                print(json_data)
                break

    sock.close()