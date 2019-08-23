import math
from .color import Color

class Palette():
    def __init__(self):
        self.current_color = Color(0,0,0)
        self.previous_color = Color(0,0,0)
        self.target_color = Color(0,0,0)
        self.animation_start_time = 0
        self.animation_length = 0

    def update(self, target_color, animation_start_time, animation_length):
        self.previous_color       = Color(self.current_color.r, self.current_color.g, self.current_color.b)
        self.target_color         = target_color
        self.animation_start_time = animation_start_time
        self.animation_length     = animation_length
    
    def lerp(self, a, b, u):
        return math.floor((1-u) * a + u * b)
    
    def color_to_render(self, now):

        color_to_render = Color(0,0,0)
        elapsed_time = now - self.animation_start_time
        animation_end_time = self.animation_start_time + self.animation_length

        if(now <= self.animation_start_time):
            color_to_render = self.current_color
        elif(now > self.animation_start_time and now < animation_end_time):
            r = self.lerp(self.previous_color.r, self.target_color.r, elapsed_time / self.animation_length)
            g = self.lerp(self.previous_color.g, self.target_color.g, elapsed_time / self.animation_length)
            b = self.lerp(self.previous_color.b, self.target_color.b, elapsed_time / self.animation_length)
            color_to_render =  Color(r,g,b)
        else:
            color_to_render  = self.target_color

        return color_to_render
