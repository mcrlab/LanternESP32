from .color import Color
from math import ceil

def transform_color(position, start_color, target_color):

    r = start_color.r + ((target_color.r - start_color.r) * position)
    g = start_color.g + ((target_color.g - start_color.g) * position)
    b = start_color.b + ((target_color.b - start_color.b) * position)

    color =  Color(r,g,b)

    return color

def calculate_color(self, start_color, target_color, position):    
    if(position <= 0):
        color_to_render = self.start_color
    elif(position > 0 and position < 1):
        color_to_render =  transform_color(position, start_color, target_color)
    else:
        color_to_render  = target_color
    return color_to_render
        
def color_to_render(current_time, start_time, end_time, render_interval):
    percent_complete    = get_percent_complete(current_time, start_time, end_time, render_interval)
    target_color        = calculate_color(percent_complete)
    return target_color


def get_percent_complete(current_time, start_time, end_time, render_interval):
    elapsed_time = current_time - start_time
    length = end_time - start_time
    if(current_time < start_time):
        return 0
    if current_time >= end_time:
        return 1
    if(length == 0):
        return 0
    else:
        fps = (1000 / render_interval)
        test =  ceil((elapsed_time / length) * fps) / fps
        return test
             