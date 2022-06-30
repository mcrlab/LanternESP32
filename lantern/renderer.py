from .color import Color

BLACK = Color(0,0,0)


class Renderer():
    def __init__(self, view, render_interval):
        self.current_color = BLACK
        self.last_render_time = 0
        self.render_interval = render_interval
        self.view = view
        self.animation = None
        

    def update_animation(self, animation):
        self.animation = animation 

    def render(self, current_time):
        if self.animation is None:
            return
        if current_time < self.animation.start_time:
            return

        if(((current_time - self.last_render_time) > self.render_interval)):
            color = self.animation.color_to_render(current_time, self.render_interval)
            self.view.render_color(color)
            self.current_color = color
            self.last_render_time = current_time       
    
    def render_color(self, color):
        self.view.render_color(color)
        self.current_color = color