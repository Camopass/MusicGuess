import io
import os

import pygame

import musicmanager
from gameviews.colors import Colors
from gameviews.gameview import GameView
from scripts.playbackcontroller import PlaybackController


class Interrogation(GameView):

    def __init__(self, game_data):
        self.game_data = game_data
        self.api_key = os.getenv("API_KEY")

        self.song = musicmanager.get_top_songs("s3nse1_snorlax", self.api_key)[0]
        self.song_audio = musicmanager.download_song(self.song)
        self.album_cover = musicmanager.get_image(self.song)
        self.song.cover = io.BytesIO(self.album_cover)

        self.album_cover = pygame.image.load(self.song.cover).convert()
        self.album_cover = pygame.transform.scale(self.album_cover, (280, 280))

        self.playback_controller = PlaybackController(self.song_audio)
        self.playback_controller.load()
        self.play_button = PlayButton(pygame.rect.Rect(500, 300, 75, 100), self.playback_controller)

        self.player_buttons = []
        for player in self.game_data.players:
            self.player_buttons.append(PlayerButton(player))

    def update(self):
        self.play_button.update()

    def render(self, screen):


        # Begin Rendering
        screen.fill(Colors.WHITE)

        # Red Background Separator
        pygame.draw.polygon(screen, Colors.RED, ((650, 0), (1280, 0), (1280, 720), (890, 720)))
        pygame.draw.aaline(screen, Colors.RED, (649, 0), (889, 720))

        # Who Listens to this Song?
        pygame.draw.rect(screen, Colors.BLUE, (118, 35, 1065, 80))
        pygame.draw.rect(screen, Colors.BLUE, (108, 25, 1065, 80))
        pygame.draw.rect(screen, Colors.WHITE, (111, 28, 1059, 74))
        courier_prime_60 = pygame.font.Font("./assets/CourierPrime-Bold.ttf", 60)
        screen.blit(courier_prime_60.render("WHO LISTENS TO THIS SONG?", True, Colors.BLUE), (180, 35))

        # Progress Bar
        pygame.draw.rect(screen, Colors.BLUE, (45, 666, 1210, 35))
        pygame.draw.rect(screen, Colors.BLUE, (35, 656, 1210, 35))

        # Album Cover
        pygame.draw.rect(screen, Colors.BLUE, (70, 180, 300, 300))
        pygame.draw.rect(screen, Colors.BLUE, (80, 190, 300, 300))

        screen.blit(self.album_cover, (80, 190, 100, 100))

        # Song Information
        space_mono_35 = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 35)
        screen.blit(space_mono_35.render(self.song.title, True, Colors.BLUE), (70, 500))
        space_mono_25 = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 25)
        screen.blit(space_mono_25.render(self.song.artist, True, Colors.BLUE), (70, 545))
        space_mono_15 = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 20)
        screen.blit(space_mono_15.render(f"Plays: {self.song.total_plays}", True, Colors.BLUE), (73, 580))

        # Play Button
        self.play_button.render(screen)

        # Choices


        # TODO: Progres bar, volume sliders

    def unload(self):
        self.playback_controller.unload()
        pygame.font.quit()


import button
import pygame


class PlayButton(button.Button):
    def __init__(self, rect, playback_controller):
        super().__init__(rect)
        self.playback_controller = playback_controller

    def render_image(self):
        surface = pygame.surface.Surface((75, 100), pygame.SRCALPHA).convert_alpha()
        pygame.draw.polygon(surface, (14, 66, 95), ((0, 0), (0, 100), (75, 50)))
        return surface

    def on_click(self):
        self.playback_controller.toggle()


class PlayerButton(button.Button):
    pass
