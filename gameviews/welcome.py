import pygame

from button import Button
from gameviews.colors import Colors
from gameviews.gameview import GameView


class WelcomeClient(GameView):
    def __init__(self, game_data):
        super().__init__()
        self.game_data = game_data
        self.courier_prime_60 = pygame.font.Font('assets/CourierPrime-Bold.ttf', 60)
        self.space_mono_60 = pygame.font.Font('assets/SpaceMono-Regular.ttf', 60)
        self.next_button = NextButton(pygame.Rect(900, 600, 350, 100), self.press_button)
        self.username_text = TextFieldCharLimit(pygame.rect.Rect(105, 255, 750, 75), 15, game_data,
                                                self.space_mono_60,(10, -5), Colors.BLUE)
        self.address_text = TextFieldCharLimit(pygame.rect.Rect(105, 455, 750, 75), 21, game_data,
                                               self.space_mono_60,(10, -5), Colors.BLUE)
        self.button_pressed = False

    def press_button(self):
        self.button_pressed = True

    def render(self, screen):
        screen.fill(Colors.WHITE)

        # Welcome
        pygame.draw.rect(screen, Colors.BLUE, (118, 35, 1065, 80))
        pygame.draw.rect(screen, Colors.BLUE, (108, 25, 1065, 80))
        pygame.draw.rect(screen, Colors.WHITE, (111, 28, 1059, 74))
        screen.blit(self.courier_prime_60.render("WELCOME TO GENREALIKE", True, Colors.BLUE), (275, 35))

        # Red Frame
        pygame.draw.lines(screen, Colors.RED, False, ((85, 600), (85, 670), (175, 670)), 5)
        pygame.draw.lines(screen, Colors.RED, False, ((1105, 160), (1195, 160), (1195, 230)), 5)
        pygame.draw.rect(screen, Colors.RED, (75, 150, 1130, 530), 5)

        # Text Labels
        screen.blit(self.space_mono_60.render("last.fm username", True, Colors.BLUE), (100, 150))
        screen.blit(self.space_mono_60.render("IP:Port", True, Colors.BLUE), (100, 350))

        # Last.fm username text box
        pygame.draw.rect(screen, Colors.BLUE, (100, 250, 760, 85))
        pygame.draw.rect(screen, Colors.BLUE, (110, 260, 760, 85))
        pygame.draw.rect(screen, (255, 255, 255), (105, 255, 750, 75))
        self.username_text.render_text(screen)

        # Address text box
        pygame.draw.rect(screen, Colors.BLUE, (100, 450, 760, 85))
        pygame.draw.rect(screen, Colors.BLUE, (110, 460, 760, 85))
        pygame.draw.rect(screen, (255, 255, 255), (105, 455, 750, 75))
        self.address_text.render_text(screen)

        self.next_button.render(screen)

    def update(self):
        self.next_button.update()
        self.username_text.update()
        self.address_text.update()

    def unload(self):
        pass


class NextButton(Button):
    def __init__(self, rect, callback):
        super().__init__(rect)
        self.space_mono_60 = pygame.font.Font('assets/SpaceMono-Regular.ttf', 60)

        self.on_click = callback

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
    def __init__(self, rect, char_limit, game_data, font, render_pos, color):
        self.text = ""
        self.char_limit = char_limit
        self.focused = False
        self.rect = rect
        self.game_data = game_data
        self.clicked_timer = 0
        self.cursor_timer = 1
        self.font = font
        self.render_pos = render_pos
        self.color = color

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.focused = True
            else:
                self.focused = False
        if self.focused:
            for event in self.game_data.game_events:
                if event.type == pygame.KEYDOWN:
                    self.clicked_timer = 1
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.text) > 0:
                            self.text = self.text[:-1]
                    else:
                        if len(self.text) < self.char_limit:
                            self.text += event.unicode
        self.clicked_timer -= self.game_data.deltaTime
        self.cursor_timer -= self.game_data.deltaTime
        if self.cursor_timer <= 0:
            self.cursor_timer = 1

    def render_text(self, screen):
        text = self.text
        cursor_char = " "
        if self.focused:
            if self.cursor_timer >= 0:
                cursor_char = "|"
            elif self.cursor_timer >= 0:
                cursor_char = "|"
        text += cursor_char
        screen.blit(self.font.render(text, True, self.color), (self.rect.x + self.render_pos[0], self.rect.y + self.render_pos[1]))


class WelcomeHost(GameView):
    def __init__(self, game_data):
        self.game_data = game_data
        self.courier_prime_60 = pygame.font.Font('assets/CourierPrime-Bold.ttf', 60)
        self.space_mono_40 = pygame.font.Font('assets/SpaceMono-Regular.ttf', 40)
        self.ready_button = ReadyButton(pygame.rect.Rect(950, 625, 300, 85), self.press_button)
        self.button_pressed = False

    def press_button(self):
        self.button_pressed = True

    def update(self):
        self.ready_button.update()

    def render(self, screen):
        screen.fill(Colors.WHITE)

        # IP ADD
        pygame.draw.rect(screen, Colors.BLUE, (118, 35, 1065, 80))
        pygame.draw.rect(screen, Colors.BLUE, (108, 25, 1065, 80))
        pygame.draw.rect(screen, Colors.WHITE, (111, 28, 1059, 74))
        screen.blit(self.courier_prime_60.render("JOIN AT IP ADDRESS HERE", True, Colors.BLUE), (225, 35))

        # Red Frame
        pygame.draw.lines(screen, Colors.RED, False, ((85, 600), (85, 670), (175, 670)), 5)
        pygame.draw.lines(screen, Colors.RED, False, ((1105, 160), (1195, 160), (1195, 230)), 5)
        pygame.draw.rect(screen, Colors.RED, (75, 150, 1130, 530), 5)

        screen.blit(self.space_mono_40.render("Players", True, Colors.BLUE), (110, 185))
        for i, player in enumerate(self.game_data.players):
            offset = i * 85
            pygame.draw.rect(screen, Colors.BLUE, (110, 260 + offset, 450, 85))
            pygame.draw.rect(screen, Colors.WHITE, (115, 265 + offset, 440, 75))
            screen.blit(self.space_mono_40.render(player.name, True, Colors.BLUE), (125, 270 + offset))

        self.ready_button.render(screen)

    def unload(self):
        pass

class ReadyButton(Button):
    def __init__(self, rect, callback):
        super().__init__(rect)
        self.space_mono_40 = pygame.font.Font('assets/SpaceMono-Regular.ttf', 40)
        self.on_click = callback

    def render_image(self):
        surface = pygame.Surface((self.rect.width, self.rect.height), flags=pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(surface, Colors.BLUE, (0, 0, self.rect.width - 10, self.rect.height - 10))
        pygame.draw.rect(surface, Colors.BLUE, (10, 10, self.rect.width - 10, self.rect.height - 10))
        pygame.draw.rect(surface, Colors.RED, (5, 5, self.rect.width - 20, self.rect.height - 20))
        surface.blit(self.space_mono_40.render("Ready!", True, Colors.WHITE), (15, 5))
        return surface

    def on_click(self):
        pass

