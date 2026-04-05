import sys

from gamedata import GameData
from gameviews.waitingforhost import WaitingForHost
from gameviews.welcome import WelcomeClient, WelcomeHost
from networking import Client, Host
from debug.networking import TEST_HOST, TEST_PORT
import gameviews
import io
from threading import Thread

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
    clock = pygame.time.Clock()
    running = True

    pygame.display.set_caption("GENREALIKE")

    game_data = GameData(clock)
    game_data.players = [Player("ThatGoblinKinga"), Player("JeremyJeremyyyy"), Player("CameronPassmore"), Player("BarackObamaAGod")]
    # view = Results(game_data, game_data.players[0], {game_data.players[0]: game_data.players[1], game_data.players[1]: game_data.players[1], game_data.players[2]: game_data.players[1], game_data.players[3]: game_data.players[1]})
    view = WelcomeHost(game_data)

    while running:
        game_data.game_events = pygame.event.get()
        for event in game_data.game_events:
            if event.type == pygame.QUIT:
                running = False

        view.update()
        view.render(screen)

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