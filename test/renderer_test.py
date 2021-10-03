from lantern.renderer import Renderer

class TestClassRenderer:
    def test_initialise(self):
        r= Renderer(5)
        assert r.number_of_pixels == 5

    def test_default_easing(self):
        r = Renderer(5)
        assert r.easing == "ElasticEaseOut"

    def test_default_buffer(self):
        r = Renderer(2)
        assert len(r.color_buffer) == 2
        color = r.color_buffer[0]
        assert color.as_hex() == "000000"
        color = r.color_buffer[1]
        assert color.as_hex() == "000000"
    
   