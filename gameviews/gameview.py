from abc import ABC, abstractmethod

class GameView(ABC):
    @abstractmethod
    def render(self, screen):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def unload(self):
        pass

