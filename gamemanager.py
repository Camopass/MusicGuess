from pygame import Surface
from networking import Host, Client, User
from displayermanager import DisplayManager

from globals import DEFAULT_HOST, DEFAULT_PORT, START_MESSAGE, END_ROUND_MESSAGE
from debug.networking import TEST_SONG
from gameviews.gamestart import  GameStart

class GameManager:

    def __init__(self, window: Surface) -> None:
        self.display_manager = DisplayManager(window, GameStart())
        self.gamestate_update = self.game_start
        self.round_started = False
    
    def make_networker(self, 
                       is_host: bool = False) -> User:
        self.networker = (Host(DEFAULT_HOST, DEFAULT_PORT) if is_host
                          else Client())
        return self.networker
    
    def gamestate_update(self, *args, **kwargs):
        pass

    def update(self, ticks):
        # self.display_manager.draw()
        self.gamestate_update(ticks)

    def game_start(self, *args):
        response = input("Are you hosting? y/N")
        is_host = response.lower() == "y"
        if is_host:
            self.networker = Host(DEFAULT_HOST, DEFAULT_PORT)
            self.playernames = self.networker.accept_connections_until_input()
            self.gamestate_update = self.pre_game
        else:
            self.networker = Client()
            ip, port, name = self.networker.prompt()
            self.name = name
            self.networker.join(ip, port, name)
            self.gamestate_update = self.pre_game
        
    def pre_game(self, *args):
        if self.networker.is_host:
            print(self.playernames)
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
            
    def round(self, ticks: int):

        if self.networker.is_host:
            if not self.round_started:
                self.networker.all_votes = {}
                self.votes_summary = {}
                for name in self.playernames:
                    self.votes_summary[name] = "Nobody?"
                self.round_start_ticks = ticks
                self.networker.broadcast_song(TEST_SONG)
                self.networker.is_accepting_votes = True
                self.round_started = True
            self.networker.manage_player_connections()

            if (ticks - self.round_start_ticks >= 5000 
                or len(self.networker.all_votes.keys()) == len(self.playernames)):
                self.gamestate_update = self.post_round
                self.networker.broadcast_to_all(END_ROUND_MESSAGE)
                self.networker.is_accepting_votes = False
                for key, value in self.networker.all_votes.items():
                    self.votes_summary[key] = value
                print(self.votes_summary)
        else:
            current_song = self.networker.recieve_song()
            print(f"Your song is {current_song}\nvote for\n{current_song.correct_player} or {' or '.join(current_song.incorrect_players)}")
            self.networker.start_round(self.name)
            self.gamestate_update = self.post_round

    def post_round(self, *args):
        pass