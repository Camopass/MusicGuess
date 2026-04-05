import pygame

from button import Button
from gameviews.colors import Colors
from gameviews.gameview import GameView


class Results(GameView):
    def __init__(self, game_data, winning_player, votes):
        super().__init__()
        self.game_data = game_data
        self.winning_player = winning_player
        self.votes = votes
        self.winning_players = []
        self.losers = []
        for player in self.votes.keys():
            if self.votes[player] == self.winning_player:
                self.winning_players.append(player)
            else:
                self.losers.append(player)
        self.next_button = NextButton(pygame.rect.Rect(930, 620, 310, 85))
        self.courier_prime_60 = pygame.font.Font("./assets/CourierPrime-Bold.ttf", 60)
        self.space_mono_35 = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 35)
        self.space_mono_20 = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 30)
        self.space_mono_small = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 20)
        self.space_mono_tiny = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 15)

    def render(self, screen):
        screen.fill(Colors.WHITE)

        # Who Was It Really ?
        pygame.draw.rect(screen, Colors.BLUE, (118, 35, 1065, 80))
        pygame.draw.rect(screen, Colors.BLUE, (108, 25, 1065, 80))
        pygame.draw.rect(screen, Colors.WHITE, (111, 28, 1059, 74))
        screen.blit(self.courier_prime_60.render("WHO WAS IT REALLY?", True, Colors.BLUE), (180, 35))

        pygame.draw.lines(screen, Colors.RED, False, ((425, 150), (75, 150), (75, 680), (1205, 680), (1205, 150), (675, 150)), 5)
        pygame.draw.lines(screen, Colors.RED, False, ((85, 600), (85, 670), (175, 670)), 5)
        pygame.draw.lines(screen, Colors.RED, False, ((1105, 160), (1195, 160), (1195, 230)), 5)
        pygame.draw.line(screen, Colors.RED, (640, 350), (640, 550), 5)

        screen.blit(self.space_mono_20.render("IT WAS...", True, Colors.BLUE), (475, 135))

        pygame.draw.rect(screen, Colors.BLUE, (450, 190, 350, 75))
        pygame.draw.rect(screen, Colors.BLUE, (460, 200, 350, 75))
        pygame.draw.rect(screen, Colors.RED, (455, 195, 340, 65))
        screen.blit(self.space_mono_35.render(self.winning_player.name, True, Colors.WHITE), (465, 195))

        screen.blit(self.space_mono_35.render("INCORRECT", True, Colors.BLUE), (1000, 155))
        screen.blit(self.space_mono_35.render("CORRECT", True, Colors.BLUE), (100, 615))

        self.next_button.render(screen)

        for i, player in enumerate(self.winning_players):
            hoffset = (i % 2) * 150
            voffset = 0 if i < 2 else 275
            pygame.draw.rect(screen, Colors.BLUE, (95 + voffset, 300 + hoffset, 250, 50))
            pygame.draw.rect(screen, Colors.BLUE, (105 + voffset, 310 + hoffset, 250, 50))
            pygame.draw.rect(screen, Colors.WHITE, (100 + voffset, 305 + hoffset, 240, 40))
            screen.blit(self.space_mono_small.render(player.name, True, Colors.BLUE), (130 + voffset, 300 + hoffset))

        for i, player in enumerate(self.losers):
            hoffset = (i % 2) * 150
            voffset = 0 if i < 2 else 275
            pygame.draw.rect(screen, Colors.BLUE, (650 + voffset, 300 + hoffset, 250, 50))
            pygame.draw.rect(screen, Colors.BLUE, (660 + voffset, 310 + hoffset, 250, 50))
            pygame.draw.rect(screen, Colors.WHITE, (655 + voffset, 305 + hoffset, 240, 40))
            screen.blit(self.space_mono_small.render(player.name, True, Colors.BLUE), (655 + voffset, 305 + hoffset))
            screen.blit(self.space_mono_tiny.render("Thought...", True, Colors.BLUE), (655 + voffset, 360 + hoffset))
            pygame.draw.rect(screen, Colors.BLUE, (750 + voffset, 350 + hoffset, 150, 30))
            pygame.draw.rect(screen, Colors.BLUE, (760 + voffset, 360 + hoffset, 150, 30))
            pygame.draw.rect(screen, Colors.WHITE, (755 + voffset, 355 + hoffset, 140, 20))
            screen.blit(self.space_mono_tiny.render(self.votes[player].name, True, Colors.BLUE), (755 + voffset, 355 + hoffset))


    def update(self):
        self.next_button.update()

    def unload(self):
        pass


class NextButton(Button):
    def __init__(self, rect):
        super().__init__(rect)
        self.space_mono_40 = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 40)

    def render_image(self):
        screen = pygame.surface.Surface(self.rect.size, pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(screen, Colors.BLUE, (0, 0, 300, 75))
        pygame.draw.rect(screen, Colors.BLUE, (10, 10, 300, 75))
        pygame.draw.rect(screen, Colors.RED, (5, 5, 290, 65))
        screen.blit(self.space_mono_40.render("Next Song", True, Colors.WHITE), (10, 5))
        return screen

    def on_click(self):
        pass
