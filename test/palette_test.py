from lantern import palette
from lantern import color

class TestClassPalette:
    def test_initialise(self):
        red = color.Color(255,0,0)
        blue  = color.Color(0,0,255)
        p = palette.Palette(red, blue)
        assert p.start_color == red
        assert p.target_color == blue
        
    def test_update(self):
        red = color.Color(255,0,0)
        blue  = color.Color(0,0,255)
        green = color.Color(0,255,0)
        yellow = color.Color(255,255,0)
        p = palette.Palette(red, blue)
        p.update(green, yellow)
        assert p.start_color == green
        assert p.target_color == yellow

        