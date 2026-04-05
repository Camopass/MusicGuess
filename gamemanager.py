from pygame import Surface
from networking import Host, Client, User
from displayermanager import DisplayManager
import threading

from globals import DEFAULT_HOST, DEFAULT_PORT, START_MESSAGE, END_ROUND_MESSAGE
from debug.networking import TEST_SONG
from gameviews import (
    clientorhostselection,
    colors,
    gameover,
    interrogation,
    results,
    waitingforhost,
    welcome
)
from gamedata import GameData

class GameManager:

    def __init__(self, window: Surface, gamedata: GameData) -> None:
        self.display_manager = DisplayManager(window, clientorhostselection.ClientOrHostSelection())
        self.gamestate_update = self.game_start
        self.round_started = False
        self.gamedata = gamedata
    
    def make_networker(self, 
                       is_host: bool = False) -> User:
        self.networker = (Host(DEFAULT_HOST, DEFAULT_PORT) if is_host
                          else Client())
        return self.networker
    
    def gamestate_update(self, *args, **kwargs):
        pass

    def update(self, ticks):
        self.gamestate_update(ticks)

    def game_start(self, *args):
        self.display_manager.draw()
        if self.display_manager.gameview.is_host == True:
            self.gamestate_update = self.welcome_host
            self.display_manager.switch_gameviews(welcome.WelcomeHost(self.gamedata))
            self.networker = Host(DEFAULT_HOST, DEFAULT_PORT)
        elif self.display_manager.gameview.is_host == False:
            self.networker = Client()            
            self.gamestate_update = self.client_get_info
            self.display_manager.switch_gameviews(welcome.WelcomeClient(self.gamedata))
    
    def welcome_host(self, *args):
        self.playernames = self.networker.accept_connections_until_true(self.display_manager.gameview.button_pressed,
                                                                        self.display_manager.draw)
        
        if self.playernames is not None:
            self.gamestate_update = self.pre_game

    def client_get_info(self, *args):
        self.display_manager.draw()

        if self.display_manager.gameview.button_pressed:
            raw = self.display_manager.gameview.address_text.text.split(":")
            ip = raw[0]
            port = int(raw[1])
            name = self.display_manager.gameview.username_text.text
            self.networker.join(ip, port, name)
            self.gamestate_update = self.pre_game
            self.display_manager.switch_gameviews(waitingforhost.WaitingForHost(self.gamedata))
        
        
    def pre_game(self, *args):
        if self.networker.is_host:
            print(self.playernames)
            print("Starting Round!")
            self.networker.is_accepting_connections = False
            self.networker.manage_player_connections()
            self.networker.broadcast_to_all(START_MESSAGE)
            self.gamestate_update = self.round
            self.display_manager.switch_gameviews(interrogation.Interrogation(self.gamedata))
        else:
            round_start_event = threading.Event()

            waiting = threading.Thread(target=lambda: self.networker.await_round_start(round_start_event), 
                             daemon=True)
            
            if not waiting.is_alive():
                waiting.start()

            self.display_manager.draw()
            self.gamestate_update = self.round
            self.display_manager.switch_gameviews(interrogation.Interrogation(self.gamedata))
            
    def round(self, ticks: int):

        if self.networker.is_host:
            if not self.round_started:
                self.display_manager.draw()
                self.networker.all_votes = {}
                self.votes_summary = {}
                for name in self.playernames:
                    self.votes_summary[name] = "Nobody?"
                self.round_start_ticks = ticks
                self.networker.broadcast_song(TEST_SONG)
                self.networker.is_accepting_votes = True
                self.round_started = True

            self.display_manager.draw()
            self.networker.manage_player_connections()

            if (ticks - self.round_start_ticks >= 30000 
                or len(self.networker.all_votes.keys()) == len(self.playernames)):
                self.gamestate_update = self.post_round
                self.networker.broadcast_to_all(END_ROUND_MESSAGE)
                self.networker.is_accepting_votes = False
                for key, value in self.networker.all_votes.items():
                    self.votes_summary[key] = value
                print(self.votes_summary)
        else:
            current_song = self.networker.recieve_song()
            self.networker.start_round(self.name, self.display_manager.draw)
            self.gamestate_update = self.post_round

    def post_round(self, *args):
        pass