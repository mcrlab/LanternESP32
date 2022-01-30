from .palette import Palette
from .animation import Animation
from .color import Color
from .easing import easings
from .easing import ElasticEaseOut as default_easing

BLACK = Color(0,0,0)

class Renderer():
    def __init__(self):
        self.palette = Palette(BLACK, BLACK)
        self.animation = Animation(0, 0)
        self.current_color = BLACK
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

    def should_draw(self):
        return self.current_color is not self.palette.target_color

    def transform_color(self, position):
        start_color  = self.palette.start_color
        target_color = self.palette.target_color

        r = start_color.r + ((target_color.r - start_color.r) * position)
        g = start_color.g + ((target_color.g - start_color.g) * position)
        b = start_color.b + ((target_color.b - start_color.b) * position)

        color =  Color(r,g,b)

        return color

    def calculate_color(self, position):    
        if(position <= 0):
            color_to_render = self.palette.start_color
        elif(position > 0 and position < 1):
            color_to_render =  self.transform_color(position)
        else:
            color_to_render  = self.palette.target_color
        self.current_color = color_to_render
        
    def color_to_render(self, now):
        completion      = self.animation.get_completion(now)
        easing_function = self.select_easing_function()
        position        = easing_function(completion)
        self.calculate_color(position)
        return self.current_color
        