import sys
from chatroom import Chatroom

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
HOST = (IP, PORT)

def get_ip_and_port():
    """Gets IP and/or Port given by the user, if the user doesn't give anything, then default values remain.
    """
    global IP, PORT, HOST
    args = sys.argv[1:]
    if args:
        print(args)
        if len(args) == 1: IP = str(args[0])
        if len(args) >= 2:
            IP = str(args[0])
            PORT = int(args[1])
        HOST = (IP, PORT)

def main():
    """ Initializes the chatroom, so it receives and sends messages in a loop.
    """
    get_ip_and_port()
    chatroom = Chatroom(HOST, HEADER_LENGTH)
    chatroom.set_up()

    while True:
        readables, exceptionals = chatroom.check_sockets()
        for socket in readables:
            if socket == chatroom.server_socket:
                chatroom.new_connection()
            else:
                message = chatroom.read_message(socket)
                if message is False: continue
                chatroom.broad_message(socket, message)
        [chatroom.remove_socket(socket) for socket in exceptionals]


if __name__ == '__main__':
    main()
