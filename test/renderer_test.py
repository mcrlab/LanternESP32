from lantern.renderer import Renderer

class TestClassRenderer:
    def test_initialise(self):
        r= Renderer()


    def test_default_easing(self):
        r = Renderer()
        assert r.easing == "ElasticEaseOut"

    
   