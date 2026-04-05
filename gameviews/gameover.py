import pygame

from button import Button
from gameviews.colors import Colors
from gameviews.gameview import GameView


class GameOver(GameView):
    def __init__(self, game_data, ranked_list):
        self.ranked_list = ranked_list
        self.courier_prime_60 = pygame.font.Font('assets/CourierPrime-Bold.ttf', 60)
        self.space_mono_50 = pygame.font.Font('assets/SpaceMono-Regular.ttf', 30)
        self.play_again_button = PlayAgainButton(pygame.rect.Rect(25, 550, 400, 150))

    def render(self, screen):
        screen.fill(Colors.WHITE)

        # Who Was It Really ?
        pygame.draw.rect(screen, Colors.BLUE, (118, 35, 1065, 80))
        pygame.draw.rect(screen, Colors.BLUE, (108, 25, 1065, 80))
        pygame.draw.rect(screen, Colors.WHITE, (111, 28, 1059, 74))
        screen.blit(self.courier_prime_60.render("LEADERBOARD", True, Colors.BLUE), (450, 35))

        # (75, 150), (75, 680), (1205, 680), (1205, 150)
        pygame.draw.lines(screen, Colors.RED, False, ((1105, 160), (1195, 160), (1195, 230)), 5)
        pygame.draw.rect(screen, Colors.RED, (75, 150, 1130, 530), 5)

        for i, player in enumerate(self.ranked_list):
            voffset = 225 * i
            hoffset = 100 * i
            pygame.draw.rect(screen, Colors.BLUE, (110 + voffset, 200 + hoffset, 350, 80))
            pygame.draw.rect(screen, Colors.BLUE, (120 + voffset, 210 + hoffset, 350, 80))
            color = Colors.WHITE
            text_color = Colors.BLUE
            if (i == 0):
                color = Colors.RED
                text_color = Colors.WHITE
            elif (i == 3):
                color = Colors.BLUE
                text_color = Colors.WHITE
            pygame.draw.rect(screen, color, (115 + voffset, 205 + hoffset, 340, 70))
            screen.blit(self.space_mono_50.render(f"{i}).{player.name}", True, text_color), (120 + voffset, 210 + hoffset))

        self.play_again_button.render(screen)

    def update(self):
        self.play_again_button.update()

    def unload(self):
        pass


class PlayAgainButton(Button):
    def __init__(self, rect):
        super().__init__(rect)
        self.space_mono_40 = pygame.font.Font('assets/SpaceMono-Regular.ttf', 40)

    def render_image(self):
        surface = pygame.Surface((self.rect.width, self.rect.height), flags=pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(surface, Colors.BLUE, (0, 0, self.rect.width - 10, self.rect.height - 10))
        pygame.draw.rect(surface, Colors.BLUE, (10, 10, self.rect.width - 10, self.rect.height - 10))
        pygame.draw.rect(surface, Colors.RED, (5, 5, self.rect.width - 20, self.rect.height - 20))
        surface.blit(self.space_mono_40.render("Play", True, Colors.WHITE), (15, 5))
        surface.blit(self.space_mono_40.render("Again?", True, Colors.WHITE), (15, 55))
        return surface

    def on_click(self):
        pass