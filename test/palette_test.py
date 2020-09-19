import os, sys
lib_dir = os.path.join(os.path.dirname(__file__), '../main/')
assert(os.path.exists(lib_dir))
sys.path.insert(0, lib_dir)

from lantern.color import Color
from lantern.palette import Palette


class TestPalette:
    def test_default_palette(self):
        now = 0
        black = Color(0,0,0)
        p = Palette(1)
        buffer  = p.color_to_render(now)
        current_color = buffer[0]
        assert current_color.as_instruction() == black.as_instruction()
        
    def test_before_animation_starts(self):
        p = Palette(1)
        now = 0
        animation_length = 10
        animation_start_time = 5  
        target_color = Color(0,0,255)
        p.update(target_color, animation_start_time, animation_length, now)

        color_buffer = p.color_to_render(now)
        calculated_color = color_buffer[0]
        assert calculated_color.as_instruction() == Color(0,0,0).as_instruction()


    def test_mid_animation(self):
        p = Palette(1)
        now = 5
        animation_length = 10
        animation_start_time = 0  
        target_color = Color(0,0,255)
        p.update(target_color, animation_start_time, animation_length, now)
        buffer  = p.color_to_render(now)
        calculated_color = buffer[0]

        assert calculated_color.r == 0
        assert calculated_color.g == 0
        assert calculated_color.b == 127
    
    def test_post_animation(self):
        p = Palette(5)
        now = 16
        animation_length = 10
        animation_start_time = 5  
        target_color = Color(0,0,255)
        p.update(target_color, animation_start_time, animation_length, now)
        color_buffer = p.color_to_render(20)
        calculated_color = color_buffer[0]
        assert calculated_color.r == 0
        assert calculated_color.g == 0
        assert calculated_color.b == 255

    # def test_light_should_animate_from_current_color(self):
    #     p = Palette(5)
    #     red = Color(255,0,0)
    #     blue = Color(0,0,255)
    #     p.update(red, 0, 0, 0)
    #     color_buffer = p.color_to_render(0)
    #     calculated_color = color_buffer[1].as_object()
    #     assert calculated_color['r'] == 255

    #     p.update(blue, 5, 5, 0)

        # color_buffer = p.color_to_render(now)
        # calculated_color = color_buffer[0]

        # assert p.color_to_render(5).r == 255
        # assert p.color_to_render(5).b == 0

        # assert p.color_to_render(10).r == 0
        # assert p.color_to_render(10).b == 255


