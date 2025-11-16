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

# very ugly main loop
if __name__ == "__main__":
    player_type = login()
    print(f"Player type: {player_type}")

    if player_type == "host":

        # TODO display TUI where host chooses game 
        # from TUI puts into choice ttt or bj
        
        choice = "ttt"
        if get_players() >= 2:
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
        # host's main loop after selection

    elif player_type == "player":
        # player's main loop
        while True:
            data = sock.recv(1024)
            if not data:
                continue
            json_str = data.decode('utf-8')
            json_data = json.loads(json_str)

            tictactoe_role = None
            if json_data['type'] == "tictactoe_confirm":
                print(json_data)
                tictactoe_role = json_data['role']
                continue;
            elif json_data['type'] == "blackjack_confirm":
                None
            elif json_data['type'] == "ttt_state_update":
                # TODO DISPLAY BOARD HERE with TUI and information from this packet
                # probably will be ugly

                print(json_data)
                if json_data['turn'] == tictactoe_role:

                    # TODO let player know its their turn
                    # tell player to click
                    # get input from player's choice in TUI
                    # and get it into row col
                    
                    row = None
                    col = None
                    packet = {"type": "ttt_action", "action": "place", "row": row, "col": col}
                    json_data = json.dumps(packet).encode('utf-8')
                    sock.sendall(json_data)
                    continue
                #pass?
                else:
                    # none of that, just keep board displayed
                    continue
                #pass?
            elif json_data['type'] == ['ttt_valid_move']:
                if json_data['valid'] == False:
                    # TODO make player choose again
                    print(json_data)
                    None
                else:
                    print(json_data)
                    continue
            elif json_data['type'] == ['ttt_result']:
                # TODO display game results in TUI with packet info
                print(json_data)
                None
            elif json_data['type'] == "bj_state_update":
                print(json_data)
                None

    sock.close()
