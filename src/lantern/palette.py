import math
from .color import Color
from .animation import Animation

class Palette():
    def __init__(self, number_of_pixels):
        self.number_of_pixels = number_of_pixels
        self.current_color = Color(0,0,0)
        self.animation = Animation(Color(0,0,0), Color(0,0,0), 0, 0)

    def update(self, target_color, animation_start_time, animation_length, now):
        previous_color = Color(self.current_color.r, self.current_color.g, self.current_color.b)
        self.animation = Animation(previous_color, target_color, animation_start_time, animation_length)
    
    def color_to_render(self, now):

        if(now <= self.animation.start_time):
            color_to_render = self.current_color
        elif(self.animation.is_animating(now)):
            color_to_render =  self.animation.color_to_render(now)
        else:
            color_to_render  = self.animation.target_color
            
        self.current_color = color_to_render

        return color_to_render
