import socket
import json
import vars
IP_ADDRESS = vars.IP_ADDRESS
PORT = vars.PORT
USERNAME = vars.USERNAME

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# encodes and sends packet dict
def send_packet(packet: dict):
    json_data = json.dumps(packet).encode('utf-8')
    sock.sendall(json_data)

# waits for next packet from server
def wait_for_packet():
    data = sock.recv(1024)
    json_str = data.decode('utf-8')
    json_data = json.loads(json_str)
    return json_data


# connects, logs in, waits for type assignment
def login():
    sock.connect((IP_ADDRESS, PORT))
    json_data = wait_for_packet()
    print(f"Connected: {json_data['accepted']}")

    packet = {"type": "login", "name": USERNAME}
    send_packet(packet)

    json_data = wait_for_packet()
    return json_data['player_type']

# get number of connected players, waits for answer
def get_players():
    packet = {"type": "numplayers"}
    send_packet(packet)

    json_data = wait_for_packet()
    return json_data['num']


# sends socket info on game choice from host
def pick_game(choice: str):
    if choice == "ttt":
        packet = {"type": "tictactoe_start"}
        send_packet(packet)
    elif choice == "bj":
        packet = {"type": "blackjack_start"}
        send_packet(packet)


# handles packet from server based on 'type' field
def handle_packet(json_data: dict):
    tictactoe_role = None
    if json_data['type'] == "tictactoe_confirm":
        
        tictactoe_role = json_data['role']

    elif json_data['type'] == "blackjack_confirm":
        None

    elif json_data['type'] == "ttt_state_update":

        # TODO DISPLAY BOARD HERE with TUI and information from this packet
        # probably will be ugly

        print(json_data)
        if json_data['state']['turn'] == tictactoe_role:

            # TODO let player know its their turn
            # tell player to click
            # get input from player's click in TUI
            # and get it into row col
            
            row = None
            col = None
            packet = {"type": "ttt_action", "action": "place", "row": row, "col": col}
            send_packet(packet)
        else:
            # none of that, just keep board displayed
            None
    elif json_data['type'] == "ttt_valid_move":
        if json_data['valid'] == False:
            
            # TODO wait for player to click again
            
            print(json_data)
            None
        else:
            print(json_data)
    elif json_data['type'] == "ttt_result":

        # TODO display game results in TUI with packet info
        
        print(json_data)
        None
    elif json_data['type'] == "bj_state_update":
        print(json_data)
        None


# main
if __name__ == "__main__":
    player_type = login()
    print(f"Player type: {player_type}")

    if player_type == "host":

        # TODO display TUI where host chooses game 
        # from TUI puts into choice ttt or bj
        
        while True:
            if get_players() >= 2:
                choice = "ttt"
                pick_game(choice)
                break

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
