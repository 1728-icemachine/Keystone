from networking.backend import Backend
from ui.app import KeystoneApp
from threading import Thread
from threading import Event
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
        self.tui.run()

    def init_cb_pool(self):
        #backend callbacks
        g.cb_pool.add("click_cell",self.net_handler.click_cell)
        g.cb_pool.add("get_players",self.net_handler.get_players)
        g.cb_pool.add("login",self.net_handler.login)
        g.cb_pool.add("start_thread",self.start_net_thread)
        #frontend callbacks
        screen = self.tui.get_screen("ttt")
        g.cb_pool.add("update_board",screen.update_board)

         
        
    def start_net_thread(self, _ = None):
        if not self.net_thread.is_alive():
            self.net_thread.start()
 
    def run_net_handler(self):
        if g.player_type == "host":
            g.my_turn_event.clear()
        else:
            g.my_turn_event.set()
        
        print(f"logged in as {player_type}")

        self.net_handler.pick_game("ttt")

        while True:
            g.my_turn_event.wait() 
            self.net_handler.listen_board_update()
            
            #self.net_handler.handle_packet(json_data)
            g.my_turn_event.clear()
        self.net_thread.join()
        self.net_handler.close_conn()




