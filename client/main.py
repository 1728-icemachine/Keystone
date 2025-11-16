import globals as g
from ui.app import MyApp

def main():
    g.init_vars()
    app = MyApp()
    app.run()
    

if __name__ == "__main__":
    main()
