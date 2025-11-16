import networking.backend as backend
import ui.app as ui
from threading import Thread
from threading import Event
import globals as g

class Client():
    
    net_handler = None
    tui = None
    tui_thread = None

    def __init__(self):
        self.tui = ui()
        self.net_handler = backend()
        self.init_cb_pool()
        self.net_thread = Thread(target = self.run_net_handler)
        self.net_thread.start()
        self.tui.run()

    def init_cb_pool():
        cb_pool.add("login",tui.login)
        

    def run_net_handler(self):
        #self.net_handler.login()
        pass




