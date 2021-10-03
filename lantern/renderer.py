from .palette import Palette
from .animation import Animation
from .color import Color
from .easing import easings
from .easing import ElasticEaseOut as default_easing

BLACK = Color(0,0,0)

class Renderer():
    def __init__(self, number_of_pixels,):
        self.number_of_pixels = number_of_pixels
        self.palette = Palette(BLACK, BLACK)
        self.animation = Animation(0, 0)
        self.current_color = BLACK
        self.color_buffer = [BLACK] * number_of_pixels
        self.easing = "ElasticEaseOut"

    def update(self, target_color, animation_start_time, animation_length, easing):
        self.animation = Animation(animation_start_time, animation_length)
        self.palette.update(self.current_color, target_color)
        self.easing = easing

    def select_easing_function(self):
        if self.easing in easings:
            return easings[self.easing]
        else:
            return default_easing

    def get_current_color(self):
        return self.palette.target_color

    def should_draw(self, now):
        return not self.animation.is_complete(now)

    def color_to_render(self, position):
        r = self.palette.start_color.r + ((self.palette.target_color.r - self.palette.start_color.r) * position)
        g = self.palette.start_color.g + ((self.palette.target_color.g - self.palette.start_color.g) * position)
        b = self.palette.start_color.b + ((self.palette.target_color.b - self.palette.start_color.b) * position)

        color =  Color(r,g,b)

        return color

    def fill(self, completion, position):    

        if(completion == 0):
            color_to_render = self.palette.start_color
        elif(completion > 0 and completion < 1):
            color_to_render =  self.color_to_render(position)
        else:
            color_to_render  = self.palette.target_color
            
        self.current_color = color_to_render
        
        self.color_buffer = [color_to_render] * self.number_of_pixels

    def buffer_to_render(self, now):
        completion = self.animation.get_completion(now)
        easing_function = self.select_easing_function()
        position = easing_function(completion)
        self.fill(completion, position)
        return self.color_buffer
        