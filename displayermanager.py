from pygame import Surface
from gameviews.gameview import GameView

class DisplayManager:
    def __init__(self,  window: Surface, 
                 gameview: GameView) -> None:
        self.window = window
        self.gameview = gameview
    
    def draw(self):
        self.gameview.render(self.window)
        self.gameview.update()
    
    def switch_gameviews(self, 
                         new_gameview: GameView) -> None:
        self.gameview.unload()
        self.gameview = new_gameview