from lantern import color
from lantern.view import View
from lantern.color import Color

class TestClassView:
    def test_initialise(self):
        view= View(1,5)
        assert view.number_of_pixels == 5

    def test_render_should_render_a_buffer_of_colors(self):
        view= View(1,3)
        colorBuffer = [Color(255,0,0), Color(0,255,0), Color(0,0,255)]
        view.render(colorBuffer)
        assert view.np[0] == (255,0,0)
        assert view.np[1] == (0,255,0)
        assert view.np[2] == (0,0,255)

    def test_render_color_should_set_all_lights_same_color(self):
        view= View(1,3)
        RED = Color(255,0,0)
        view.render_color(RED)
        assert view.np[0] == (255,0,0)
        assert view.np[1] == (255,0,0)
        assert view.np[2] == (255,0,0)

    def test_off_should_turn_off_all_lights(self):
        view= View(1,3)
        RED = Color(255,0,0)
        view.render_color(RED)
        view.off()
        assert view.np[0] == (0,0,0)
        assert view.np[1] == (0,0,0)
        assert view.np[2] == (0,0,0)

   