from chatroom import Chatroom

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
ADDRESS = (IP, PORT)


def main():
    """ Initializes the chatroom, so it reads and sends messages in a loop.
    """
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

