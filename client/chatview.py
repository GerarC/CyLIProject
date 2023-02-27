import errno
import threading
import tkinter as tk
from tkinter import simpledialog
from chatclient import ChatClient

class ChatView:
    """Chat client view.
    
    Args:
        root (tkinter.Tk): parent window.
        host (tuple): a pair with the IP address as first element and the port as second.
        headlen (int): the size of the message header.
    """
    def __init__(self, root: tk.Tk, host: tuple, headlen: int):
        self._frame = tk.Frame(root)
        self._username = str(
            simpledialog.askstring(
                'Nombre de Usuario',
                'Entra tu nombre de usuario, por favor.',
                parent=root
            ))
        self._chat_client = ChatClient(
            self._username,
            host=host,
            header_length=headlen
        )

    def initialize(self):
        """Initializes the application and all that make it works and sets the running state as True.
        """
        self._frame.grid()
        self._chat_client.set_up()
        self._create_widgets()
        self._locate_widgets()
        self._insert_message(f'Bienvenido a este chat, {self._username}!\n')
        self.running = True
        self.loop = threading.Thread(target=self._reload)
        self.loop.start()

    def stop(self):
        """ Set the running state as False and end the thread of receive data.
        """
        self.running = False
        self.loop.join()

    def _reload(self):
        """Reloads self._messages_text when a message is received.
        """
        while self.running:
            try:
                message = self.receive_message()
                self._insert_message('\n' + message)

            except IOError as err:
                if  err.errno != errno.EAGAIN and err.errno != errno.EWOULDBLOCK:
                    print("Reading Error", str(err))
                    return
                continue

            except Exception as e:
                print("General Error", str(e))
                return

    def _create_widgets(self):
        """ Initialize all the needed widgets.
        """
        self._title_lbl = tk.Label(
            self._frame,
            text='Chatroom C&L',
            font='Helvetica 14 bold'
        )
        self._username_lbl = tk.Label(
            self._frame,
            text=self._username,
            font='Helvetica 10'
        )
        # Send Messages
        self._message_lbl = tk.Label(
            self._frame,
            text='Mensaje:',
            font='Helvetica 12'
        )
        self._message_entry = tk.Entry(
            self._frame,
            font='Helvetica 12'
        )
        self._message_entry.config(width=30)
        self._message_btn = tk.Button(
            self._frame,
            text='Enviar',
            font='Helvetica 12',
            command=self.send_message
        )
        self._message_entry.bind(
            '<Return>',
            lambda event=None: self.send_message()
        )
        # View Messages
        self._messages_view = tk.Text(
            self._frame,
            font='Helvetica 12'
        )
        self._messages_scroll = tk.Scrollbar(self._frame)
        self._messages_scroll.config(
            command=self._messages_view.yview
        )
        self._messages_view.config(
            width=48,
            height=30,
            yscrollcommand=self._messages_scroll.set,
            state=tk.DISABLED
        )

    def _locate_widgets(self):
        """Locates all the widgets of the application.
        """
        self._title_lbl.grid(padx=5, row=0, column=1, columnspan=2)
        self._username_lbl.grid(padx=5, row=0, column=3)

        self._message_lbl.grid(padx=5, row=1, column=0, sticky='W')
        self._message_entry.grid(padx=5, row=1, column=1, columnspan=2)
        self._message_btn.grid(padx=5, row=1, column=3)

        self._messages_view.grid(padx=5, row=2, column=0, columnspan=4, rowspan=5)
        self._messages_scroll.grid(row=2, column=4, rowspan=5, sticky='ENS')

    def _insert_message(self, message: str):
        """Unblocks message_view, inserts the given message, and blocks it again.

        Args:
            message (str): message to be inserted.
        """
        self._messages_view.config(state=tk.NORMAL)
        self._messages_view.insert(tk.END, message)
        self._messages_view.config(state=tk.DISABLED)

    def send_message(self):
        """Reads the content of the message entry and sends it through chat client.
        """
        message = self._message_entry.get()
        self._message_entry.delete(0, tk.END)
        self._chat_client.send_message(message)
        self._insert_message(f'\n{self._username}(Yo)> {message}')

    def receive_message(self):
        """Receives user and message via chat client, and formats it.

        Returns:
            data (str): the user and the message in the same string.
        """
        user = self._chat_client.receive_username()
        message = self._chat_client.receive_message()
        data = f'{user}> {message}'

        return data
