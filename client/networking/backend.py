import socket
import json
import globals as g

class Backend():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

     
    def close_conn(self):
        if self.sock:
            self.sock.close()

    # encodes and sends packet dict
    def send_packet(self, packet: dict):
        json_data = json.dumps(packet).encode('utf-8')
        return self.sock.sendall(json_data)

    # waits for next packet from server
    def wait_for_packet(self):
        data = self.sock.recv(1024)
        json_str = data.decode('utf-8')
        json_data = json.loads(json_str)
        return json_data

    def listen_board_update(self):
        json_data = wait_for_packet()
        board = json_data["board"]
        g.cb_pool.call("update_board",board)

    # connects, logs in, waits for type assignment
    def login(self, _ = None):
        self.sock.connect((g.ip_address, g.port))
        json_data = self.wait_for_packet()
        print(f"Connected: {json_data['accepted']}")

        packet = {"type": "login", "name": g.username}
        self.send_packet(packet)

        json_data = self.wait_for_packet()
        return json_data['player_type']

    # get number of connected players, waits for answer
    def get_players(self, _ = None):
        packet = {"type": "numplayers"}
        self.send_packet(packet)

        json_data = self.wait_for_packet()
        return json_data['num']


    # sends socket info on game choice from host
    def pick_game(self,choice: str):
        if choice == "ttt":
            packet = {"type": "tictactoe_start"}
            self.send_packet(packet)
        elif choice == "bj":
            packet = {"type": "blackjack_start"}
            self.send_packet(packet)


    # handles packet from server based on 'type' field
    def click_cell(self, pos : tuple ):
        row = pos[0]
        col = pos[1]
        packet = {"type": "ttt_action", "action": "place", "row": row, "col": col}
        return self.send_packet(packet)
        

    def handle_packet(self, json_data: dict):
        tictactoe_role = None
        if json_data['type'] == "tictactoe_confirm":
            
            tictactoe_role = json_data['role']

        elif json_data['type'] == "blackjack_confirm":
            pass

        elif json_data['type'] == "ttt_state_update":

            pass

            ## TODO DISPLAY BOARD HERE with TUI and information from this packet
            ## probably will be ugly

            #print(json_data)
            #if json_data['state']['turn'] == tictactoe_role:

            #    # TODO let player know its their turn
            #    # tell player to click
            #    # get input from player's click in TUI
            #    # and get it into row col
            #    
            #    row = None
            #    col = None
            #    packet = {"type": "ttt_action", "action": "place", "row": row, "col": col}
            #    send_packet(packet)
            #else:
            #    # none of that, just keep board displayed
            #    None
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
#if __name__ == "__main__":
#    g.player_type = login()
#    print(f"Player type: {g.player_type}")
#
#    if g.player_type == "host":
#
#        # TODO display TUI where host chooses game 
#        # from TUI puts into choice ttt or bj
#        
#        while True:
#            if get_players() >= 2:
#                choice = "ttt"
#                pick_game(choice)
#                break
#
#        while True:
#            json_data = wait_for_packet()
#            handle_packet(json_data)
#           
#    elif g.player_type == "player":
#        
#        while True:
#            json_data = wait_for_packet()
#            handle_packet(json_data)
#       
#    sock.close()
