from "../src/color" import Color
from "../src/color" import calculate_color

class TestClassColor:
    def test_initialise(self):
        color = Color(255,128, 0)
        assert color.r == 255
        assert color.g == 128
        assert color.b == 0

    def test_instruction(self):
        color = Color(255,128, 0)
        assert color.instruction() == (255,128,0)

class TestCalculateColor:
    def test_before_animation_starts(self):
        now = 0
        animation_length = 10
        animation_start_time = 5  
        previous_color = Color(255,0,0)
        current_color = Color(255,0,0)
        target_color = Color(0,0,255)
        
        calculated_color = calculate_color(now, animation_length, animation_start_time, previous_color, current_color, target_color)
        assert calculated_color == current_color

    def test_mid_animation(self):
        now = 5
        animation_length = 10
        animation_start_time = 0  
        previous_color = Color(255,0,0)
        current_color = Color(255,0,0)
        target_color = Color(0,0,255)
        
        calculated_color = calculate_color(now, animation_length, animation_start_time, previous_color, current_color, target_color)
        assert calculated_color.r == 127
        assert calculated_color.g == 0
        assert calculated_color.b == 127
        

    def test_before_animation_starts(self):
        now = 16
        animation_length = 10
        animation_start_time = 5  
        previous_color = Color(255,0,0)
        current_color = Color(255,0,0)
        target_color = Color(0,0,255)
        
        calculated_color = calculate_color(now, animation_length, animation_start_time, previous_color, current_color, target_color)
        assert calculated_color == target_color