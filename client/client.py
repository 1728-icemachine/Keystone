from networking.backend import Backend
from ui.app import KeystoneApp
from threading import Thread
from threading import Event
from utils.debug import pfile
import time
import globals as g

class Client():
    
    net_handler = None
    tui = None
    net_thread = None

    def __init__(self):
        self.tui = KeystoneApp()
        self.net_handler = Backend()
        self.init_cb_pool()
        self.net_thread = Thread(target = self.run_net_handler)

    def start_client(self):
        with open("DEBUG.txt", "w") as f:
            pass

        #self.net_thread.start()
        self.tui.run()
        #self.net_thread.join()

    def init_cb_pool(self):
        #backend callbacks
        g.cb_pool.add("click_cell",self.net_handler.click_cell)
        g.cb_pool.add("get_players",self.net_handler.get_players)
        g.cb_pool.add("login",self.net_handler.login)
        g.cb_pool.add("start_thread",self.start_net_thread)
        g.cb_pool.add("pick_game",self.net_handler.pick_game)
        g.cb_pool.add("wait_for_packet",self.net_handler.wait_for_packet)
        g.cb_pool.add("send_packet", self.net_handler.send_packet)
        #frontend callbacks
        screen = self.tui.get_screen("ttt")# doesnt even work
        g.cb_pool.add("update_board",screen.update_board)
        
    def start_net_thread(self, _ = None):
        pfile("STARTING THREAD")

        self.net_thread.start()
 
    def run_net_handler(self):
        #time.sleep(1)
        #self.tui.push_screen("ttt")
        #return
        pfile("in nethandler")
        g.my_turn_event.clear()
        if g.player_type == "player":
            pfile("p")
            json_data = self.net_handler.wait_for_packet()# should be confirm packet
            send_data = {"type":"tictactoe_trigger"}
            g.cb_pool.call("send_packet",send_data)
            pfile("received conf in player")
            pfile(f"{json_data}")
            json_type = json_data['type']
            pfile(f"{json_type} == tictactoe_confirm")
            evalo = json_data['type'] == "tictactoe_confirm"
            pfile(f"evaluated to {evalo}")
            if json_data['type'] == "tictactoe_confirm":
                pfile(f"{g.player_type} tictactoe_cofnfirm should be player")
                #--- FAILS HERE --
                #AHHHH
                self.tui.push_screen("ttt")
                #AHHH
                pfile(f"{g.player_type} pushed screen")
                self.net_handler.listen_board_update() # init booard packt

        else:
            pfile("host_event blocking")
            g.my_turn_event.wait()
            g.my_turn_event.set()
        
        pfile("yayayyay")
        #json_data = self.net_handler.wait_for_packet()# should be confirm packet
        #self.net_handler.handle_packet(json_data)# does nothing rn
        #self.net_handler.listen_board_update() # init booard packt

        while True:
            g.my_turn_event.wait() 
            self.net_handler.listen_board_update()
            
            #self.net_handler.handle_packet(json_data)
            g.my_turn_event.clear()
        self.net_thread.join()
        self.net_handler.close_conn()




