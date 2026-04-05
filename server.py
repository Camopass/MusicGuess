import socket
import pygame
import requests


class ServerNetworking:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 6967))
        self.clients = []
