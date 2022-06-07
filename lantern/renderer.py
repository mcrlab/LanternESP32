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

    def check_and_render(self, current_time):
        if self.animation is None:
            return

        if(((current_time - self.last_render_time) > self.render_interval)):
            if(self.current_color is not self.animation.palette.target_color):
                color = self.animation.color_to_render(current_time)
                self.view.render_color(color)
                self.current_color = color
                self.last_render_time = current_time       