import socket
import sys


class ChatClient:
    """ A Class that wraps a socket.

    Args:
        username (str): the name of the current user.
        address (tuple): address of the listening host.
        header_length (int): used header length.

    """
    def __init__(self, username: str, address: tuple, header_length: int = 10) -> None:
        self._header_length = header_length
        self._username = username.encode('utf-8')
        self._username_header = f"{len(self._username):<{self._header_length}}".encode('utf-8')
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_up(self):
        """Connects the client to the chatclient address.
        """
        self._socket.connect(self._address)
        self._socket.setblocking(False)
        self._socket.send(self._username_header + self._username)

    @property
    def client_socket(self):
        """ Returns the server socket of the chatroom.
        """
        return self._socket

    def send_message(self, text: str):
        if text:
            message  = text.encode('utf-8')
            message_header = f"{len(message):<{self._header_length}}".encode('utf-8')
            self._socket.send(message_header + message)

    def receive_username(self):
        username_header = self._socket.recv(self._header_length)
        if not len(username_header):
            print('Connection closed by the server')
            sys.exit()
        username_length = int(username_header.decode('utf-8'))
        username = self._socket.recv(username_length).decode('utf-8')
        return username

    def receive_message(self):
        message_header = self._socket.recv(self._header_length)
        message_length = int(message_header.decode('utf-8'))
        message = self._socket.recv(message_length).decode('utf-8')
        return message
