import pygame

from button import Button
from gameviews.colors import Colors
from gameviews.gameview import GameView


class WelcomeClient(GameView):
    def __init__(self, game_data, clock):
        super().__init__()
        self.game_data = game_data
        self.courier_prime_60 = pygame.font.Font('assets/CourierPrime-Bold.ttf', 60)
        self.space_mono_60 = pygame.font.Font('assets/SpaceMono-Regular.ttf', 60)
        self.next_button = NextButton(pygame.Rect(900, 600, 350, 100))
        self.clock = clock
        self.username_text = TextFieldCharLimit(self.next_button.rect, 8, clock)

    def render(self, screen):
        screen.fill(Colors.WHITE)

        # CLIENT OR HOST?
        pygame.draw.rect(screen, Colors.BLUE, (118, 35, 1065, 80))
        pygame.draw.rect(screen, Colors.BLUE, (108, 25, 1065, 80))
        pygame.draw.rect(screen, Colors.WHITE, (111, 28, 1059, 74))
        screen.blit(self.courier_prime_60.render("WELCOME TO GENREALIKE", True, Colors.BLUE), (275, 35))

        pygame.draw.lines(screen, Colors.RED, False, ((85, 600), (85, 670), (175, 670)), 5)
        pygame.draw.lines(screen, Colors.RED, False, ((1105, 160), (1195, 160), (1195, 230)), 5)
        pygame.draw.rect(screen, Colors.RED, (75, 150, 1130, 530), 5)

        screen.blit(self.space_mono_60.render("last.fm username", True, Colors.BLUE), (100, 150))
        screen.blit(self.space_mono_60.render("IP:Port", True, Colors.BLUE), (100, 350))

        pygame.draw.rect(screen, Colors.BLUE, (100, 250, 550, 85))
        pygame.draw.rect(screen, Colors.BLUE, (110, 260, 550, 85))
        pygame.draw.rect(screen, (255, 255, 255), (105, 255, 540, 75))

        pygame.draw.rect(screen, Colors.BLUE, (100, 450, 550, 85))
        pygame.draw.rect(screen, Colors.BLUE, (110, 460, 550, 85))
        pygame.draw.rect(screen, (255, 255, 255), (105, 455, 540, 75))

        self.next_button.render(screen)

    def update(self):
        self.next_button.update()

    def unload(self):
        pass


class NextButton(Button):
    def __init__(self, rect):
        super().__init__(rect)
        self.space_mono_60 = pygame.font.Font('assets/SpaceMono-Regular.ttf', 60)

    def on_click(self):
        pass

    def render_image(self):
        surface = pygame.Surface((self.rect.width, self.rect.height), flags=pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(surface, Colors.BLUE, (0, 0, self.rect.width - 10, self.rect.height - 10))
        pygame.draw.rect(surface, Colors.BLUE, (10, 10, self.rect.width - 10, self.rect.height - 10))
        pygame.draw.rect(surface, Colors.RED, (5, 5, self.rect.width - 20, self.rect.height - 20))
        surface.blit(self.space_mono_60.render("Next", True, Colors.WHITE), (15, 0))

        return surface


class TextFieldCharLimit:
    def __init__(self, rect, char_limit, clock):
        self.text = ""
        self.char_limit = char_limit
        self.focused = False
        self.rect = rect
        self.clock = clock

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.focused = True
            else:
                self.focused = False
        if self.focused:
            pass # pygame.key.

