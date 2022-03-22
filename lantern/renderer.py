try:
    from time import ticks_ms
except (ImportError, ModuleNotFoundError) as e:
    from mocks import ticks_ms

from .palette import Palette
from .animation import Animation
from .color import Color
from .easing import easings
from .easing import ElasticEaseOut as default_easing

BLACK = Color(0,0,0)

class Renderer():
    def __init__(self, view, render_interval):
        self.palette = Palette(BLACK, BLACK)
        self.animation = Animation(0, 0)
        self.current_color = BLACK
        self.easing = "ElasticEaseOut"
        self.last_render_time = 0
        self.render_interval = render_interval
        self.view = view

    def update_animation(self, data):
        current_time = ticks_ms()

        color = Color(0,0,0)
        color.from_hex(data['color'])
        animation_length = data['time']
        animation_start_time = current_time

        if 'easing' in data:
            easing = data['easing']
        else:
            easing = "ElasticEaseOut"

        self.update(color, animation_start_time, animation_length, easing) 


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

    def check_and_render(self, current_time):
        if(((current_time - self.last_render_time) > self.render_interval)):
            if(self.should_draw()):
                color = self.color_to_render(current_time)
                self.view.render_color(color)
                self.last_render_time = current_time       