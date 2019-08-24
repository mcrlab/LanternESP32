import os, sys
fake_dir = os.path.join(os.path.dirname(__file__), 'fake')
assert(os.path.exists(fake_dir))
sys.path.insert(0, fake_dir)

from src.view import View
from src.color import Color

class TestClassView():
    def test_intialisation(self):
        pin = 0
        number_of_pixels = 16
        v = View(pin, number_of_pixels)
        assert v.number_of_pixels == number_of_pixels

    def test_render(self):
        current_time = 15
        pin = 0
        number_of_pixels = 16
        v = View(pin, number_of_pixels)
        v.render(Color(0,0,0), current_time)
        assert v.last_render_time == current_time     
