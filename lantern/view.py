try:
    from neopixel import NeoPixel
except (ModuleNotFoundError, ImportError) as e:
    from mocks import NeoPixel
    
from .color import HexColor
BLACK = HexColor("000000")
class View():
    def __init__(self, pin, number_of_pixels):
        self.number_of_pixels = number_of_pixels
        self.np = NeoPixel(pin, self.number_of_pixels)  
        self.current_color = BLACK
        
    def render_color(self, color):
        self.current_color = color
        self.np.fill(color)
        self.np.write()
        
    def render(self):
        pass

    def off(self):
        self.render_color(BLACK)
