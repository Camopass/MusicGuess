import socket
import selectors
import types

class User:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, 
                                    socket.SOCK_STREAM)
    
    def __del__(self):
        self.socket.close()

class Host(User):
    """A User who runs the game, acts a server."""

    def __init__(self, 
                 HOST: str, 
                 PORT: int) -> None:
        super().__init__()
        self.socket.bind((HOST, PORT))
        self.selector = selectors.DefaultSelector()
        self.player_names = []

    def listen(self):
        self.socket.listen()
        self.socket.setblocking(False)
        self.selector.register(self.socket, selectors.EVENT_READ, data=None)

    def register_accepted_sockets(self, user_socket: socket.socket):
        connection, address = user_socket.accept()
        connection.setblocking(False)
        data = types.SimpleNamespace(addr=address, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(connection, events, data=data)
    
    def manage_player_connections(self):
        events = self.selector.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                self.register_accepted_sockets(key.fileobj) # pyright: ignore[reportArgumentType]
            else:
                self.handle_connection(key, mask)
    
    def write_to_player(self, user_socket, socket_data):
        if socket_data.outb:
            sent = user_socket.send(socket_data.outb)
            socket_data.outb = socket_data.outb[sent:]

    def read_from_player(self, socket_data, recieved_data):
        socket_data.outb += recieved_data

    def handle_connection(self, 
                          key: selectors.SelectorKey, 
                          mask):
        client_socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recieved_data = client_socket.recv(1024) # pyright: ignore[reportAttributeAccessIssue]
            if recieved_data:
                self.read_from_player(data, recieved_data)
            else:
                self.selector.unregister(client_socket)
                client_socket.close() # pyright: ignore[reportAttributeAccessIssue]
        if mask & selectors.EVENT_WRITE:
            self.write_to_player(client_socket, data)
                

    def __del__(self):
        self.selector.close()
        return super().__del__()

class Client(User):
    """A User who joins a host"""

    def prompt(self):

        raw_input = input("IP:Port -> ").split(":")
        ip = raw_input[0]
        port = int(raw_input[1])
        return (ip, port)

    def join(self, HOST, PORT):
        self.socket.connect((HOST, PORT))
    
    def send_and_recieve_test(self):
        self.socket.sendall(bytes(input(), encoding='utf-8'))
        return self.socket.recv(1024)