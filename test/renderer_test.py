from lantern import renderer
from lantern.renderer import Renderer
from lantern.color import Color


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

    def test_calculate_color_should_set_start_color_if_not_started(self):
        r = Renderer()
        target_color = Color(0,0,255)

        animation_start_time = 0
        animation_length = 10
        easing = "EaseOutBounce"
        r.update(target_color, animation_start_time, animation_length, easing)
        r.calculate_color(0)
        assert r.current_color == Color(0,0,0)

    def test_calculate_color_should_calculate_color_if_in_animation(self, mocker):
        r = Renderer()
        target_color = Color(0,0,255)

        def mock_calculate(self, position):
            return Color(255,255,255)

        mocker.patch('lantern.renderer.Renderer.transform_color', 
        mock_calculate)

        animation_start_time = 0
        animation_length = 10
        easing = "EaseOutBounce"
        r.update(target_color, animation_start_time, animation_length, easing)
        r.calculate_color(0.5)
        assert r.current_color == Color(255,255,255)

    def test_calculate_color_should_set_end_color_if_ended(self):
        r = Renderer()
        target_color = Color(0,0,255)

        animation_start_time = 0
        animation_length = 10
        easing = "EaseOutBounce"
        r.update(target_color, animation_start_time, animation_length, easing)
        r.calculate_color(1)
        assert r.current_color == target_color


    def test_transform_color(self):
        r = Renderer()
        target_color = Color(255,255,255)

        animation_start_time = 0
        animation_length = 10
        easing = "EaseOutBounce"
        r.update(target_color, animation_start_time, animation_length, easing)
        calculated_color = r.transform_color(0.5)
        assert calculated_color == Color(127,127,127)
    
    def test_update(self):
        assert True

    def test_select_easing_function(self):
        from lantern.easing import easings
        assert True
    
   