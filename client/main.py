import sys
import threading
from chatview import ChatView
from tkinter import Tk

# Socket configuration
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
ADDRESS = (IP, PORT)

# View Configuration
WIDTH = 200
HEIGHT = 300

def get_ip_and_port():
    global IP, PORT, ADDRESS
    args = sys.argv[1:]
    if args:
        print(args)
        if len(args) == 1: IP = str(args[0])
        if len(args) == 2:
            IP = str(args[0])
            PORT = int(args[1])
        ADDRESS = (IP, PORT)

def main():
    root = Tk()
    root.title("Chatroom C&L")
    root.config(width=WIDTH, height=HEIGHT)
    get_ip_and_port()
    print(ADDRESS)
    chat_view = ChatView(root, address=ADDRESS, headlen=HEADER_LENGTH)
    chat_view.initialize()
    root.mainloop()
    chat_view.stop()

if __name__ == '__main__':
    main()
