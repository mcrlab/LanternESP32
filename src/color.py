import math
import time

class Color():
    def __init__(self, r,g,b):
        self.r = r
        self.g = g
        self.b = b

    def  instruction(self):
        return (self.r, self.g, self.b)
        
def lerp(a, b, u):
    return math.floor((1-u) * a + u * b)

def calculate_color(now, 
            animation_length, 
            animation_start_time, 
            previous_color,
            current_color,
            target_color):

    color_to_render = Color(0,0,0)
    elapsed_time = now - animation_start_time
    animation_end_time = animation_start_time + animation_length

    if(now < animation_start_time):
        color_to_render = current_color
    elif(now > animation_start_time and now < animation_end_time):
        r = lerp(previous_color.r, target_color.r, elapsed_time / animation_length)
        g = lerp(previous_color.g, target_color.g, elapsed_time / animation_length)
        b = lerp(previous_color.b, target_color.b, elapsed_time / animation_length)
        color_to_render =  Color(r,g,b)
    else:
        color_to_render  = target_color

    return color_to_render

def render(color, numberOfPixels):
    global np
    global last_render_time

    for i in range(numberOfPixels):
        np[i] = color.instruction()
    
    np.write() 
    last_render_time = time.ticks_ms()