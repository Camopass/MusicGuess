import button
import pygame


class PlayButton(Button.Button):
    def __init__(self, rect, playback_controller):
        super().__init__(rect)
        self.playback_controller = playback_controller

    def render_image(self):
        surface = pygame.surface.Surface((75, 100), pygame.SRCALPHA).convert_alpha()
        pygame.draw.polygon(surface, (14, 66, 95), ((0, 0), (0, 100), (75, 50)))
        return surface

    def on_click(self):
        self.playback_controller.toggle()