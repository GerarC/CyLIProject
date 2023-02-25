import sys
from chatroom import Chatroom

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
ADDRESS = (IP, PORT)

def get_ip_and_port():
    global IP, PORT, ADDRESS
    args = sys.argv[1:]
    if args:
        print(args)
        if len(args) == 1: IP = str(args[0])
        if len(args) >= 2:
            IP = str(args[0])
            PORT = int(args[1])
        ADDRESS = (IP, PORT)

def main():
    """ Initializes the chatroom, so it reads and sends messages in a loop.
    """
    get_ip_and_port()
    chatroom = Chatroom(ADDRESS, HEADER_LENGTH)
    chatroom.set_up()

    while True:
        readable, exceptional = chatroom.check_sockets()

        for notified_socket in readable:
            if notified_socket == chatroom.server_socket:
                chatroom.new_connection()
            else:
                message = chatroom.read_message(notified_socket)
                if message is False: continue
                chatroom.broad_message(notified_socket, message)

        for notified_socket in exceptional:
            chatroom.remove_socket(notified_socket)


if __name__ == '__main__':
    main()

