import os, sys

lib_dir = os.path.join(os.path.dirname(__file__), '../main/')
assert(os.path.exists(lib_dir))
sys.path.insert(0, lib_dir)

from lantern.animation import Animation
from lantern.color import Color

class TestClassAnimation():

    def test_animation_takes_a_color_start_time_and_length(self):
        previous_color = Color(0,0,0)
        target_color = Color(0,0,0)
        start_time = 0
        length = 0

        animation = Animation(previous_color, target_color, start_time, length)

        assert animation.previous_color == previous_color
        assert animation.target_color == target_color
        assert animation.start_time == start_time
        assert animation.length == length
    
    def test_is_animating_returns_false_if_not_started(self):
        previous_color = Color(0,0,0)
        target_color = Color(0,0,0)
        start_time = 5
        length = 0

        animation = Animation(previous_color, target_color, start_time, length)   
        assert animation.is_animating(4) == False

    def test_is_animating_returns_false_if_completed(self):
        previous_color = Color(0,0,0)
        target_color = Color(0,0,0)
        start_time = 5
        length = 5

        animation = Animation(previous_color, target_color, start_time, length)   
        assert animation.is_animating(10) == False

    def test_is_animating_returns_true_if_stated_but_not_completed(self):
        previous_color = Color(0,0,0)
        target_color = Color(0,0,0)
        start_time = 5
        length = 5

        animation = Animation(previous_color, target_color, start_time, length)   
        assert animation.is_animating(6) == True
