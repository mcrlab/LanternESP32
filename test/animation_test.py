from lantern import animation

class TestClassAnimation:
    def test_initialise(self):
        a = animation.Animation(10, 20)
        assert a.start_time == 10
        assert a.length == 20

    def test_is_complete(self):
        a = animation.Animation(10, 20)
        assert a.is_complete(10) == False

        a = animation.Animation(10, 20)
        assert a.is_complete(20) == False

        a = animation.Animation(10, 20)
        assert a.is_complete(30) == False

        a = animation.Animation(10, 20)
        assert a.is_complete(31) == True

        
    def test_is_animating_should_not_animate_before_starting(self):
        a = animation.Animation(10, 20)
        assert a.is_animating(9) == False

    def test_is_animating_should_not_animate_after_ending(self):
        a = animation.Animation(10, 20)
        assert a.is_animating(31) == False

    def test_is_animating_should_not_animate_after_ending(self):
        a = animation.Animation(10, 20)
        assert a.is_animating(31) == False

    def test_get_completion_should_return_0_before_starting(self):
        a = animation.Animation(10, 20)
        assert a.get_completion(9) == 0

    def test_get_completion_should_return_fraction_part_way(self):
        a = animation.Animation(10, 20)
        assert a.get_completion(20) == 0.5

    def test_get_completion_should_return_one_on_end(self):
        a = animation.Animation(10, 20)
        assert a.get_completion(30) == 1.0

    def test_get_completion_should_return_one_after_end(self):
        a = animation.Animation(10, 20)
        assert a.get_completion(50) == 1.0