from .easing import easings
from .easing import ElasticEaseOut as default_easing
from .color import Color
from .queue import Node
from math import ceil
from .logging import logger
def transform_color(position, start_color, target_color):

    r = start_color.r + ((target_color.r - start_color.r) * position)
    g = start_color.g + ((target_color.g - start_color.g) * position)
    b = start_color.b + ((target_color.b - start_color.b) * position)

    color =  Color(r,g,b)

    return color

class Animation(Node):
    def __init__(self, start_time, length, easing, palette):
        super().__init__()
        self.start_time = start_time
        self.length = length
        self.easing = easing
        self.palette = palette
        self.end_time = start_time + length

        if easing in easings:
            self.easing_fn =  easings[easing]
        else:
            self.easing_fn = default_easing

    def set_start_color(self, color):
        self.palette.start_color = color

    def get_target_color(self):
        return self.palette.target_color

    def get_end_time(self):
        return self.end_time
    
    def is_complete(self, current_time, render_interval):
        return self.get_percent_complete(current_time, render_interval) == 1

    def calculate_color(self, position):    
        if(position <= 0):
            color_to_render = self.palette.start_color
        elif(position > 0 and position < 1):
            color_to_render =  transform_color(position, self.palette.start_color, self.palette.target_color)
        else:
            color_to_render  = self.palette.target_color
        return color_to_render
        
    def color_to_render(self, current_time, render_interval):

        percent_complete    = self.get_percent_complete(current_time, render_interval)
        position            = self.easing_fn(percent_complete)
        target_color        = self.calculate_color(position)
        return target_color


    def get_percent_complete(self, current_time, render_interval):
        elapsed_time = current_time - self.start_time
        if(current_time < self.start_time):
            return 0
        if current_time >= self.end_time:
            return 1
        if(self.length == 0):
            return 0
        else:
            fps = (1000 / render_interval)
            test =  ceil((elapsed_time / self.length) * fps) / fps
            return test
             