import socket
import pygame


class ClientNetworking:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def join(self, ip, port, name):
        pass
