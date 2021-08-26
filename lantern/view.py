from neopixel import NeoPixel
from .color import Color

class View():
    def __init__(self, pin, number_of_pixels):
        self.number_of_pixels = number_of_pixels
        self.np = NeoPixel(pin, self.number_of_pixels)  
        self.last_render_time = 0
        
    def render(self, color_buffer, current_time):
        for i in range(len(color_buffer)):
            self.np[i] = color_buffer[i].as_instruction()
        
        self.np.write()
        self.last_render_time = current_time

    def render_color(self, color):
        print(color.as_hex())
        for i in range(self.number_of_pixels):
            self.np[i] = color.as_instruction()
        self.np.write()

    def off(self):
        self.render_color(Color(0,0,0))