from src.color import Color
from src.palette import Palette


class TestPalette:
    def test_default_palette(self):
        now = 0
        black = Color(0,0,0)
        p = Palette()
        current_color = p.color_to_render(now)
        assert current_color.instruction() == black.instruction()
        
    def test_before_animation_starts(self):
        p = Palette()
        now = 0
        animation_length = 10
        animation_start_time = 5  
        target_color = Color(0,0,255)
        p.update(target_color, animation_start_time, animation_length)

        calculated_color = p.color_to_render(now)
        assert calculated_color.instruction() == Color(0,0,0).instruction()


    def test_mid_animation(self):
        p = Palette()
        now = 5
        animation_length = 10
        animation_start_time = 0  
        target_color = Color(0,0,255)
        p.update(target_color, animation_start_time, animation_length)
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
        p.update(target_color, animation_start_time, animation_length)
        calculated_color = p.color_to_render(now)
        assert calculated_color.r == 0
        assert calculated_color.g == 0
        assert calculated_color.b == 255
