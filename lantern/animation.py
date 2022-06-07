from .easing import easings
from .easing import ElasticEaseOut as default_easing
from .color import Color


def transform_color(position, start_color, target_color):

    r = start_color.r + ((target_color.r - start_color.r) * position)
    g = start_color.g + ((target_color.g - start_color.g) * position)
    b = start_color.b + ((target_color.b - start_color.b) * position)

    color =  Color(r,g,b)

    return color


class Animation():
    def __init__(self, start_time, length, easing, palette):
        self.start_time = start_time
        self.length = length
        self.easing = easing
        self.palette = palette

        if easing in easings:
            self.easing_fn =  easings[easing]
        else:
            self.easing_fn = default_easing

    def calculate_color(self, position):    
        if(position <= 0):
            color_to_render = self.palette.start_color
        elif(position > 0 and position < 1):
            color_to_render =  transform_color(position, self.palette.start_color, self.palette.target_color)
        else:
            color_to_render  = self.palette.target_color
        return color_to_render
        
    def color_to_render(self, current_time):
        completion      = self.get_completion(current_time)
        position        = self.easing_fn(completion)
        target_color    = self.calculate_color(position)
        return target_color


    def get_completion(self, current_time):
        elapsed_time = current_time - self.start_time
        if(current_time < self.start_time):
            return 0
        if current_time >= self.start_time + self.length:
            return 1
        if(self.length == 0):
            return 0
        else:
            return elapsed_time / self.length