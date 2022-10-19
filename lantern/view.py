try:
    from neopixel import NeoPixel
except (ModuleNotFoundError, ImportError) as e:
    from mocks import NeoPixel
    
from .color import Color

class View():
    def __init__(self, pin, number_of_pixels):
        self.number_of_pixels = number_of_pixels
        self.np = NeoPixel(pin, self.number_of_pixels)  
        self.current_color = Color(0,0,0)
        
    def render_color(self, color):
        self.current_color = color
        for i in range(self.number_of_pixels):
            self.np[i] = color.as_instruction()
        self.np.write()
        
    def render(self):
        pass

    def off(self):
        self.render_color(Color(0,0,0))
