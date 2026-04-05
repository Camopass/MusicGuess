import pygame
import imageio_ffmpeg as ffmpeg

from scripts import Audio


class PlaybackController:
    def __init__(self, audio):
        self.audio = audio
        self.loaded = False
        self.playing = False
        self.paused = False
        self.mixer = None
        self.last_pos = 0
        self.duration = -1

    def load(self):
        self.audio = Audio.aac_to_ogg(self.audio)
        self.duration = Audio.get_length(self.audio)
        pygame.mixer.music.load(self.audio)
        self.loaded = True

    def play(self):
        if self.playing and self.paused:
            self.paused = False
            pygame.mixer.music.unpause()
        if self.playing:
            self.paused = False
            pygame.mixer.music.play()

    def pause(self):
        if self.playing and not self.paused:
            self.paused = True
            self.last_pos = pygame.mixer.music.get_pos()
            pygame.mixer.music.pause()

    def stop(self):
        self.playing = False
        self.paused = False
        pygame.mixer.music.stop()

    def get_progress(self):
        if self.loading:
            pos = self.last_pos + pygame.mixer.music.get_pos()
            return pos / self.duration

    def on_end(self):
        self.playing = False
        self.paused = False
        self.last_pos = 0

    def unload(self):
        pygame.mixer.music.unload()
        self.loaded = False

    def toggle(self):
        if self.playing and not self.paused:
            self.pause()
        else:
            self.play()
