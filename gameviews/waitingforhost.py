import pygame

from gameviews.colors import Colors
from gameviews.gameview import GameView


class WaitingForHost(GameView):
    def __init__(self, game_data):
        self.game_data = game_data
        self.font = pygame.font.Font('assets/CourierPrime-Bold.ttf', 80)

    def render(self, screen):
        screen.fill(Colors.WHITE)

        pygame.draw.lines(screen, Colors.RED, False, ((85, 600), (85, 670), (175, 670)), 5)
        pygame.draw.lines(screen, Colors.RED, False, ((1105, 60), (1195, 60), (1195, 130)), 5)
        pygame.draw.rect(screen, Colors.RED, (75, 50, 1130, 630), 5)

        screen.blit(self.font.render("Waiting for host...", True, Colors.BLUE), (175, 280))

    def update(self):
        pass

    def unload(self):
        pass

