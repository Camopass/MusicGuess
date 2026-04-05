from typing import Union
from pygame import Surface
from networking import Host, Client, User
from displayermanager import DisplayManager

from globals import DEFAULT_HOST, DEFAULT_PORT, START_MESSAGE, GameStateIDs
from debug.networking import TEST_SONG
from gameviews.gamestart import  GameStart

class GameManager:

    def __init__(self, window: Surface) -> None:
        self.display_manager = DisplayManager(window, GameStart())
        self.gamestate_update = self.game_start
    
    def make_networker(self, 
                       is_host: bool = False) -> User:
        self.networker = (Host(DEFAULT_HOST, DEFAULT_PORT) if is_host
                          else Client())
        return self.networker
    
    def gamestate_update(self):
        pass

    def update(self):
        # self.display_manager.draw()
        self.gamestate_update()

    def game_start(self):
        response = input("Are you hosting? y/N")
        is_host = response.lower() == "y"
        if is_host:
            self.networker = Host(DEFAULT_HOST, DEFAULT_PORT)
            self.connections = self.networker.accept_connections_until_input()
            self.gamestate_update = self.pre_game
        else:
            self.networker = Client()
            ip, port = self.networker.prompt()
            self.networker.join(ip, port)
            self.gamestate_update = self.pre_game
        
    def pre_game(self):
        if self.networker.is_host:
            print("Starting Round!")
            self.networker.is_accepting_connections = False
            self.networker.manage_player_connections()
            self.networker.broadcast_to_all(START_MESSAGE)
            self.gamestate_update = self.round
        else:
            print("Waiting for host to start the game!")
            self.networker.await_round_start()
            print("Starting Round!")
            self.gamestate_update = self.round

        
    def round(self):
        if self.networker.is_host:
            print("Starting Round! (for real this time)")
            self.networker.broadcast_song(TEST_SONG)
            self.networker.manage_player_connections()
        else:
            print(self.networker.recieve_song())