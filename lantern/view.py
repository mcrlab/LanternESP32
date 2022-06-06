try:
    from neopixel import NeoPixel
except (ModuleNotFoundError, ImportError) as e:
    from mocks import NeoPixel
    
from .color import Color

class View():
    def __init__(self, pin, number_of_pixels):
        self.number_of_pixels = number_of_pixels
        self.np = NeoPixel(pin, self.number_of_pixels)  
        
    def render_buffer(self, color_buffer):
        for i in range(len(color_buffer)):
            self.np[i] = color_buffer[i].as_instruction()
        
        self.np.write()

    def render_color(self, color):
        for i in range(self.number_of_pixels):
            self.np[i] = color.as_instruction()
        self.np.write()

    def off(self):
        self.render_color(Color(0,0,0))
