import sys

from gamedata import GameData
from gamemanager import GameManager
from gameviews.interrogation import Interrogation
from networking import Client, Host
from debug.networking import TEST_HOST, TEST_PORT
import gameviews
import io
from threading import Thread

import musicmanager
import os
from dotenv import load_dotenv, find_dotenv
import pygame

def main():
    load_dotenv(find_dotenv())


    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    # game_data = GameData()
    # view = Interrogation(game_data)
    gm = GameManager(screen)

    while running:
        gm.update()


    pygame.quit()



if __name__ == '__main__':
    main()