import math
from .color import Color
from .animation import Animation

class Palette():
    def __init__(self):
        self.current_color = Color(0,0,0)
        self.previous_color = Color(0,0,0)
        
        self.target_color = Color(0,0,0)
        self.animation_start_time = 0
        self.animation_length = 0

        self.animation = Animation(Color(0,0,0), Color(0,0,0), 0, 0)


    def update(self, target_color, animation_start_time, animation_length, now):
        previous_color            = Color(self.current_color.r, self.current_color.g, self.current_color.b)

        self.previous_color       = previous_color
        self.target_color         = target_color
        self.animation_start_time = animation_start_time
        self.animation_length     = animation_length

        self.animation = Animation(previous_color, target_color, animation_start_time, animation_length)
    
    def color_to_render(self, now):

        if(now <= self.animation.start_time):
            color_to_render = self.current_color
        elif(self.animation.is_animating(now)):
            color_to_render =  self.animation.color_to_render(now)
        else:
            color_to_render  = self.target_color
            
        self.current_color = color_to_render

        return color_to_render
