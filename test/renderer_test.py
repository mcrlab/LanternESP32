from lantern import renderer
from lantern.renderer import Renderer

class TestClassRenderer:
    def test_initialise(self):
        r= Renderer()
        assert isinstance(r, Renderer)


    def test_default_easing(self):
        r = Renderer()
        assert r.easing == "ElasticEaseOut"
    
    def test_creates_blank_animation(self):
        from lantern.animation import Animation
        r = Renderer()
        assert isinstance(r.animation, Animation)
    def test_creates_blank_palette(self):
        from lantern.palette import Palette
        r = Renderer()
        assert isinstance(r.palette, Palette)
    def test_default_color_is_black(self):
        r = Renderer()
        from lantern.color import Color
        black = Color(0,0,0)
        assert r.current_color == black

    
   