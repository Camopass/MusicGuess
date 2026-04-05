import socket
import selectors
import types
import json
from enum import IntEnum
from typing import Callable, Union
import threading
from song import Song
from globals import GameStateIDs

class User:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, 
                                    socket.SOCK_STREAM)
    
    def __del__(self):
        self.socket.close()

    @property
    def is_host(self) -> bool:
        return isinstance(self, Host)
    
    def recieve(self):
        length = int.from_bytes(self.recieve_bytes(4), "little")
        return self.__parse_to_json(self.recieve_bytes(length))
    
    def recieve_bytes(self, n_bytes: int):
        data = b""
        while len(data) < n_bytes:
            chunk = self.socket.recv(n_bytes - len(data))
            if not chunk:
                raise ConnectionError("Disconnected")
            data += chunk
        return data
    
    @staticmethod
    def __parse_to_json(data: bytes):
        return json.loads(data.decode("utf-8"))
    
    @staticmethod
    def format_message(message: bytes):
        return len(message).to_bytes(4, "little") + message[0:]


class Host(User):
    """A User who runs the game, acts as a server."""

    def __init__(self, 
                 HOST: str, 
                 PORT: int) -> None:
        super().__init__()
        self.socket.bind((HOST, PORT))
        self.selector = selectors.DefaultSelector()
        self.is_accepting_connections = True

    def listen(self):
        self.socket.listen()
        self.socket.setblocking(False)
        self.socket.settimeout(1.0)
        self.selector.register(self.socket, selectors.EVENT_READ, data=None)

    def register_accepted_sockets(self, client_socket: socket.socket):
        connection, address = client_socket.accept()
        print(f"{address} Connected")
        connection.setblocking(False)
        data = types.SimpleNamespace(addr=address, player_name=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(connection, events, data=data)
        return client_socket
    
    def accept_connections_until_input(self):
        stop_event = threading.Event()
        self.listen()
        connections = set()

        def wait_for_stop():
            while True:
                if input():
                    stop_event.set()
                    break
        threading.Thread(target=wait_for_stop, daemon=True).start()

        while not stop_event.is_set():
            try:
                connections.add(self.manage_player_connections())
            except socket.timeout:
                pass
        
        return connections

    def manage_player_connections(self):
        events = self.selector.select(timeout=1)
        for key, mask in events:
            if (key.data is None
                and self.is_accepting_connections):
                self.register_accepted_sockets(key.fileobj) # pyright: ignore[reportArgumentType]
            else:
                self.handle_connection(key, mask)
    
    def write_to_player(self, user_socket, socket_data):
        if socket_data.outb:
            sent = user_socket.send(socket_data.outb)
            socket_data.outb = socket_data.outb[sent:]

    def broadcast_to_all(self, 
                         data: bytes):
            for key in self.selector.get_map().values():
                if (key.data is not None):
                    key.data.outb += self.format_message(data)

    def broadcast_song(self,
                       song: Song):
        self.broadcast_to_all(song.json_mesasge)

    def handle_connection(self, 
                          key: selectors.SelectorKey, 
                          mask):
        client_socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recieved_data = client_socket.recv(1024) # pyright: ignore[reportAttributeAccessIssue]
            if recieved_data:
                pass
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
    def __init__(self):
        super().__init__()

    @staticmethod
    def prompt():
        raw_input = input("IP:Port -> ").split(":")
        ip = raw_input[0]
        port = int(raw_input[1])
        return (ip, port)

    def join(self, HOST, PORT):
        self.socket.connect((HOST, PORT))
    
    def send_and_recieve_test(self):
        self.socket.sendall(bytes(input(), encoding='utf-8'))
    
    def recieve_song(self):
        data = self.recieve()
        assert data['type'] == "song"
        return Song.from_json(data)

    def await_round_start(self):
        round_start = False
        while not round_start:
            data = self.recieve()
            round_start = (data["type"] == "gamestate"
                           and data["state"] == GameStateIDs.IN_ROUND)
