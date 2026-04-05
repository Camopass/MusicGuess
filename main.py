import sys

from gamedata import GameData
from gameviews.waitingforhost import WaitingForHost
from gameviews.welcome import WelcomeClient
from networking import Client, Host
from debug.networking import TEST_HOST, TEST_PORT
from dotenv import load_dotenv, find_dotenv
import pygame

from scripts.player import Player


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

# پخاشپپثی شمه تهاشیه قشزهسپ
def main():
    load_dotenv(find_dotenv())


    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    pygame.display.set_caption("GENREALIKE")

    game_data = GameData()
    game_data.players = [Player("Jeremy"), Player("Gus"), Player("Cameron"), Player("BarackO")]
    # view = Results(game_data, game_data.players[0], {game_data.players[0]: game_data.players[1], game_data.players[1]: game_data.players[1], game_data.players[2]: game_data.players[1], game_data.players[3]: game_data.players[1]})
    view = WaitingForHost(game_data)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        view.update()
        view.render(screen)

        pygame.display.flip()
        clock.tick(60)

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