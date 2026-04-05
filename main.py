from gamemanager import GameManager
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