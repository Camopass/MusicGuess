import sys

from gamedata import GameData
from gameviews.interrogation import Interrogation
from networking import Client, Host
from debug.networking import TEST_HOST, TEST_PORT
from dotenv import load_dotenv, find_dotenv
import pygame

def client():
    p = Client()
    HOST, PORT = p.prompt()
    p.join(HOST, PORT)
    while True:
        print(f"Got Back: {p.send_and_recieve_test()!r}")

def host():
    print("Launching as host...")
    h = Host(TEST_HOST, TEST_PORT)
    h.listen()
    while True:
        h.manage_player_connections()

def main():
    load_dotenv(find_dotenv())


    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    game_data = GameData()
    view = Interrogation(game_data)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        view.update()
        view.render(screen)

        pygame.display.flip()
        clock.tick(60)

    view.unload()

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