from abc import abstractmethod, ABC

import pygame


class Button(ABC):
    def __init__(self, rect):
        self.rect = rect
        self.hovered = False
        self.clicked = False
        self.clicked_last = False

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            else:
                self.clicked = False
        else:
            self.hovered = False
        if (not self.clicked) and self.clicked_last:
            self.on_click()
        self.clicked_last = self.clicked

    def render(self, screen):
        image = self.render_image()
        if self.clicked:
            image = pygame.transform.smoothscale(image, (self.rect.width - 10, self.rect.height - 10))
            screen.blit(image, (self.rect.x+5, self.rect.y+5))
        elif self.hovered:
            image = pygame.transform.smoothscale(image, (self.rect.width + 10, self.rect.height + 10))
            screen.blit(image, (self.rect.x-5, self.rect.y-5))
        else:
            screen.blit(image, (self.rect.x, self.rect.y))

    @abstractmethod
    def render_image(self):
        pass

    @abstractmethod
    def on_click(self):
        pass