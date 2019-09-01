import math
from .color import Color

class Animation():
    def __init__(self, previous_color, target_color, start_time, length):
        self.previous_color = previous_color
        self.target_color = target_color
        self.start_time = start_time
        self.length = length

    def lerp(self, a, b, u):
        return math.floor((1-u) * a + u * b)
    
    def is_animating(self, now):
        return (now > self.start_time) and now < (self.start_time + self.length)

    def color_to_render(self, current_time):
        elapsed_time = current_time - self.start_time

        r = self.lerp(self.previous_color.r, self.target_color.r, elapsed_time / self.length)
        g = self.lerp(self.previous_color.g, self.target_color.g, elapsed_time / self.length)
        b = self.lerp(self.previous_color.b, self.target_color.b, elapsed_time / self.length)
        color =  Color(r,g,b)

        return color

