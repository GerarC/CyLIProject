import socket
import select

class Chatroom():
    """Class that manages the server socket of a simple chat room.

    Args:
        address (tuple): a pair of host and port where will be the socket listens.
        header_length (int): the used length for the header.
    """
    def __init__(self, address: tuple, header_length: int = 10) -> None:
        self._header_length = header_length
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._known_sockets = [self._socket]
        self._clients = {}

    def set_up(self):
        """Sets the server up listening on the class address.
        """
        self._socket.bind(self._address)
        self._socket.listen()

    @property
    def server_socket(self):
        """ Returns the server socket of the chatroom.
        """
        return self._socket

    def receive(self, client_socket: socket.socket):
        """Receives the header the message, if there is a header, then see the message length and receive the entire data.

        Args:
            client_socket (socket.socket): socket where the data is received.

        Return:
            message (dict): the header and the complete data of the message.
            False (bool): returns false if there is not message.
        """
        try:
            message_header = client_socket.recv(self._header_length)
            if not len(message_header): return False

            message_length = int(message_header.decode("utf-8"))
            message = {"header": message_header, "data": client_socket.recv(message_length)}
            return message
        except:
            return False

    def check_sockets(self):
        """Checks which sockets are readables, which are writable and which have errors.
        Returns:
            readables: readable sockets.
            exceptional: sockets that have any error.
        """
        readables, _, exceptional = select.select(self._known_sockets, [], self._known_sockets)
        return readables, exceptional

    def new_connection(self):
        """ Connects a new socket and adds it to the known sockets.
        """
        client_socket, client_address = self._socket.accept()
        user = self.receive(client_socket)
        if user is False: return

        self._known_sockets.append(client_socket)
        self._clients[client_socket] = user

        print(f"New connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")

    def remove_socket(self, socket: socket.socket) -> None:
        """Removes de given socket from the clients and the known sockets.
        """
        self._known_sockets.remove(socket)
        del self._clients[socket]


    def read_message(self, client_socket: socket.socket):
        """Receive data from the given socket, if there is data return it, if there isn't removes the socket.
        Args:
            client_socket (sockets.socket): the socket where receive data.

        Return:
            message (bytes): the received message.
            False (bool): if there is no message.
        """
        message = self.receive(client_socket)
        print(message)
        if message is False:
            print(f"closed connection from {self._clients[client_socket]['data'].decode('utf-8')}")
            self.remove_socket(client_socket)
            return False
        user = self._clients[client_socket]
        print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
        return user['header'] + user['data'] + message['header'] + message['data']


    def broad_message(self, source: socket.socket, message: bytes):
        """Send the given message to all the client servers.
        Args:
            source (socket.socket): it's the source of the message and will be ignore.
            message (bytes): message to send.
        """
        for client_socket in self._clients:
            if client_socket != source: client_socket.send(message)
