from threading import Event
from call_back_pool import CallBackPool
def init_vars():
    global username
    username = "No name"
    global player_type
    player_type = None
    global ip_address
    ip_address = "127.0.0.1" # "192.168.0.233"
    global port
    port = 8080
    global my_turn_event
    my_turn_event = Event()
    global cb_pool
    cb_pool = CallBackPool()

