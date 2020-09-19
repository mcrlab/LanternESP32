from .color import Color

class Palette():
    def __init__(self):
        self.start_color = Color(0,0,0)
        self.target_color = Color(0,0,0)

    def update(self, start_color, target_color):
        self.start_color = start_color
        self.target_color = target_color

    
    
