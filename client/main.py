import globals as g
from client import Client

def main():
    g.init_vars()
    client = Client()
    client.start_client()

if __name__ == "__main__":
    main()
