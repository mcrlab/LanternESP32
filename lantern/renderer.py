from .timer import get_current_time
from .palette import Palette
from .animation import Animation
from .color import Color

BLACK = Color(0,0,0)


def transform_color(position, start_color, target_color):

    r = start_color.r + ((target_color.r - start_color.r) * position)
    g = start_color.g + ((target_color.g - start_color.g) * position)
    b = start_color.b + ((target_color.b - start_color.b) * position)

    color =  Color(r,g,b)

    return color

class Renderer():
    def __init__(self, view, render_interval):
        self.palette = Palette(BLACK, BLACK)
        self.current_color = BLACK
        self.last_render_time = 0
        self.render_interval = render_interval
        self.view = view

    def update_animation(self, data):
        current_time = get_current_time()

        target_color = Color(0,0,0)
        target_color.from_hex(data['color'])
        animation_length = data['time']
        animation_start_time = current_time

        if 'easing' in data:
            easing = data['easing']
        else:
            easing = "ElasticEaseOut"

        self.animation = Animation(animation_start_time, animation_length, easing)
        self.palette.update(self.current_color, target_color)


    def calculate_color(self, position):    
        if(position <= 0):
            color_to_render = self.palette.start_color
        elif(position > 0 and position < 1):
            color_to_render =  transform_color(position, self.palette.start_color, self.palette.target_color)
        else:
            color_to_render  = self.palette.target_color
        return color_to_render
        
    def color_to_render(self, current_time):
        completion      = self.animation.get_completion(current_time) #TODO combine these two
        position        = self.animation.easing_fn(completion)
        target_color    = self.calculate_color(position)
        return target_color

    def check_and_render(self, current_time):
        if(((current_time - self.last_render_time) > self.render_interval)):
            if(self.current_color is not self.palette.target_color):
                color = self.color_to_render(current_time)
                self.view.render_color(color)
                self.current_color = color
                self.last_render_time = current_time       