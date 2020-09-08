import os, sys
lib_dir = os.path.join(os.path.dirname(__file__), '../src/')
assert(os.path.exists(lib_dir))
sys.path.insert(0, lib_dir)

from lantern.color import Color
from lantern.palette import Palette


class TestPalette:
    def test_default_palette(self):
        now = 0
        black = Color(0,0,0)
        p = Palette()
        current_color = p.color_to_render(now)
        assert current_color.as_instruction() == black.as_instruction()
        
    def test_before_animation_starts(self):
        p = Palette()
        now = 0
        animation_length = 10
        animation_start_time = 5  
        target_color = Color(0,0,255)
        p.update(target_color, animation_start_time, animation_length, now)

        calculated_color = p.color_to_render(now)
        assert calculated_color.as_instruction() == Color(0,0,0).as_instruction()


    def test_mid_animation(self):
        p = Palette()
        now = 5
        animation_length = 10
        animation_start_time = 0  
        target_color = Color(0,0,255)
        p.update(target_color, animation_start_time, animation_length, now)
        calculated_color = p.color_to_render(now)
        assert calculated_color.r == 0
        assert calculated_color.g == 0
        assert calculated_color.b == 127
    
    def test_post_animation(self):
        p = Palette()
        now = 16
        animation_length = 10
        animation_start_time = 5  
        target_color = Color(0,0,255)
        p.update(target_color, animation_start_time, animation_length, now)
        calculated_color = p.color_to_render(now)
        assert calculated_color.r == 0
        assert calculated_color.g == 0
        assert calculated_color.b == 255

    def test_light_should_animate_from_current_color(self):
        p = Palette()
        red = Color(255,0,0)
        blue = Color(0,0,255)
        p.update(red, 0, 0, 0)
        calculated_color = p.color_to_render(1)
        assert calculated_color.r == 255
        p.update(blue, 5, 5, 0)
        assert p.color_to_render(5).r == 255
        assert p.color_to_render(5).b == 0

        assert p.color_to_render(10).r == 0
        assert p.color_to_render(10).b == 255


