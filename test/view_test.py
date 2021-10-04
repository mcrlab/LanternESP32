from lantern.view import View

class TestClassView:
    def test_initialise(self):
        view= View(1,5)
        assert view.number_of_pixels == 5

   