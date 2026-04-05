import pygame

from button import Button
from gameviews.colors import Colors
from gameviews.gameview import GameView


class ClientOrHostSelection(GameView):
    def __init__(self):
        super().__init__()
        self.client_button = ClientButton(pygame.Rect(125, 300, 450, 150), self.client_button_callback)
        self.host_button = HostButton(pygame.Rect(700, 300, 450, 150), self.host_button_callback)
        self.courier_prime_60 = pygame.font.Font('assets/CourierPrime-Bold.ttf', 60)
        self.is_host = None

    def host_button_callback(self): self.is_host = True

    def client_button_callback(self):
        self.is_host = False

    def update(self):
            self.client_button.update()
            self.host_button.update()

    def render(self, screen):
        screen.fill(Colors.WHITE)

        # CLIENT OR HOST?
        pygame.draw.rect(screen, Colors.BLUE, (118, 35, 1065, 80))
        pygame.draw.rect(screen, Colors.BLUE, (108, 25, 1065, 80))
        pygame.draw.rect(screen, Colors.WHITE, (111, 28, 1059, 74))
        screen.blit(self.courier_prime_60.render("JOINING OR HOSTING?", True, Colors.BLUE), (325, 35))

        # (75, 150), (75, 680), (1205, 680), (1205, 150)
        pygame.draw.lines(screen, Colors.RED, False, ((85, 600), (85, 670), (175, 670)), 5)
        pygame.draw.lines(screen, Colors.RED, False, ((1105, 160), (1195, 160), (1195, 230)), 5)
        pygame.draw.rect(screen, Colors.RED, (75, 150, 1130, 530), 5)

        self.client_button.render(screen)
        self.host_button.render(screen)

    def unload(self):
        pass


class ClientButton(Button):
    def __init__(self, rect, callback):
        super().__init__(rect)
        self.space_mono_40 = pygame.font.Font('assets/SpaceMono-Regular.ttf', 40)
        self.callback = callback

    def render_image(self):
        surface = pygame.Surface((self.rect.width, self.rect.height), flags=pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(surface, Colors.BLUE, (0, 0, self.rect.width - 10, self.rect.height - 10))
        pygame.draw.rect(surface, Colors.BLUE, (10, 10, self.rect.width - 10, self.rect.height - 10))
        pygame.draw.rect(surface, Colors.RED, (5, 5, self.rect.width - 20, self.rect.height - 20))
        surface.blit(self.space_mono_40.render("CLIENT", True, Colors.WHITE), (15, 5))
        return surface

    def on_click(self):
        self.callback()
        return False

class HostButton(Button):
    def __init__(self, rect, callback):
        self.space_mono_40 = pygame.font.Font('assets/SpaceMono-Regular.ttf', 40)
        self.on_click = callback
        super().__init__(rect)

    def render_image(self):
        surface = pygame.Surface((self.rect.width, self.rect.height), flags=pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(surface, Colors.BLUE, (0, 0, self.rect.width - 10, self.rect.height - 10))
        pygame.draw.rect(surface, Colors.BLUE, (10, 10, self.rect.width - 10, self.rect.height - 10))
        pygame.draw.rect(surface, Colors.RED, (5, 5, self.rect.width - 20, self.rect.height - 20))
        surface.blit(self.space_mono_40.render("HOST", True, Colors.WHITE), (15, 5))
        return surface

    def on_click(self):
        return True