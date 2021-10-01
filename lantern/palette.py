from .color import Color

class Palette():
    def __init__(self, start_color, target_color):
        self.start_color = start_color
        self.target_color = target_color

    def update(self, start_color, target_color):
        self.start_color = start_color
        self.target_color = target_color

    
    
