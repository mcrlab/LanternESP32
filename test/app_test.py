import os, sys

lib_dir = os.path.join(os.path.dirname(__file__), '../src/')
assert(os.path.exists(lib_dir))
sys.path.insert(0, lib_dir)

fake_dir = os.path.join(os.path.dirname(__file__), 'fake')
assert(os.path.exists(fake_dir))
sys.path.insert(0, fake_dir)

from lantern.app import App

class TestClassApp():
    def test_initialisation(self):
        a = App(1,2)
        assert 1 == 1