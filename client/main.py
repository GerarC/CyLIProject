import sys
from chatview import ChatView
from tkinter import Tk

# Socket configuration
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
HOST = (IP, PORT)

# View Configuration
WIDTH = 200
HEIGHT = 300

def get_ip_and_port():
    """Gets IP and/or Port given by the user, if the user doesn't give anything, then default values remain.
    """
    global IP, PORT, HOST
    args = sys.argv[1:]
    if args:
        print(args)
        if len(args) == 1: IP = str(args[0])
        if len(args) == 2:
            IP = str(args[0])
            PORT = int(args[1])
        HOST = (IP, PORT)

def main():
    """ Runs the application.
    """
    root = Tk()
    root.title("Chatroom C&L")
    root.config(width=WIDTH, height=HEIGHT)
    get_ip_and_port()
    print(HOST)
    chat_view = ChatView(root, host=HOST, headlen=HEADER_LENGTH)
    chat_view.initialize()
    root.mainloop()
    chat_view.stop()

if __name__ == '__main__':
    main()
