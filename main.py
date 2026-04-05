import sys

from gamedata import GameData
from gameviews.clientorhostselection import ClientOrHostSelection
from gameviews.gameover import GameOver
from gameviews.interrogation import Interrogation
from gameviews.results import Results
from gameviews.waitingforhost import WaitingForHost
from gameviews.welcome import WelcomeClient, WelcomeHost
from networking import Client, Host
from debug.networking import TEST_HOST, TEST_PORT
import gameviews
import io
from threading import Thread
from gamemanager import GameManager

import musicmanager
import os
from dotenv import load_dotenv, find_dotenv
import pygame

from scripts.player import Player


def client():
    p = Client()
    HOST, PORT = p.prompt()
    p.join(HOST, PORT)
    while True:
        print(f"Got Back: {p.parse_recieved_bytes(p.recieve())}")

def host():
    print("Launching as host...")
    h = Host("0.0.0.0", TEST_PORT)
    h.listen()
    Thread(target= h.send_test, daemon=True).start()
    while True:
        h.manage_player_connections()

# پخاشپپثی شمه تهاشیه قشزهسپ
def main():
    load_dotenv(find_dotenv())


    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_icon(pygame.image.load("assets/appicon.png"))
    clock = pygame.time.Clock()
    running = True

    pygame.display.set_caption("GENREALIKE")

    

    game_data = GameData(clock)
    game_data.players = [Player("ThatGoblinKinga"), Player("JeremyJeremyyyy"), Player("CameronPassmore"), Player("BarackObamaAGod")]
    # view = Results(game_data, game_data.players[0], {game_data.players[0]: game_data.players[0], game_data.players[1]: game_data.players[0], game_data.players[2]: game_data.players[1], game_data.players[3]: game_data.players[0]})
    game_manager = GameManager(screen, game_data)
    view = ClientOrHostSelection()

    while running:
        game_data.game_events = pygame.event.get()
        for event in game_data.game_events:
            if event.type == pygame.QUIT:
                running = False

        game_manager.update(pygame.time.get_ticks)

        pygame.display.flip()
        game_data.deltaTime = game_data.clock.tick(60) / 1000

    view.unload()

    pygame.font.quit()
    pygame.quit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        main()
    elif sys.argv[1] == "client":
        client()
    elif sys.argv[1] == 'host':
        host()
    else:
        main()