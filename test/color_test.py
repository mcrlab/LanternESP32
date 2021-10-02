from lantern import color

class TestClassColor:
    def test_initialise(self):
        c = color.Color(255,128, 0)
        assert c.r == 255
        assert c.g == 128
        assert c.b == 0
    
    def test_from_hex(self):
        c = color.Color(0, 0, 0)
        c.from_hex("FF00FF")
        assert c.r == 255
        assert c.g == 0
        assert c.b == 255

    def test_as_instruction(self):
        c = color.Color(255,128, 0)
        assert c.as_instruction() == (255,128,0)

    def test_to_object(self):
        c = color.Color(255, 0, 255)
        assert c.as_object() == {"r": 255, "g": 0, "b": 255}

    def test_normalise_should_not_affect_color_less_than_target_single_color(self):
        c = color.Color(255,0,0)
        c.normalise(512)
        assert c.as_object() == { "r": 255, "g": 0, "b": 0}

    def test_normalise_should_not_affect_color_less_than_target_multi_color(self):
        c = color.Color(255,255,0)
        c.normalise(512)
        assert c.as_object() == { "r": 255, "g": 255, "b": 0}

    def test_normalise_should_affect_color_greater_than_target(self):
        c = color.Color(255,255,255)
        c.normalise(512)
        assert c.as_object() == { "r": 170, "g": 170, "b": 170}