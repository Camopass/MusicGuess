import sys

from gameviews.interrogation import Interrogation
from networking import Client, Host
from debug.networking import TEST_HOST, TEST_PORT
import gameviews
import io
from threading import Thread

import MusicManager
import os
from dotenv import load_dotenv, find_dotenv
import pygame

from scripts.playbutton import PlayButton
from scripts.playbackcontroller import PlaybackController

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

def main():
    load_dotenv(find_dotenv())


    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    view = Interrogation()

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