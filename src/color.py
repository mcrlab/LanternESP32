import math


class Color():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def normalise(self, maximum_brightness):
        total = self.r + self.g + self.b
        if (total > maximum_brightness):
            fraction = maximum_brightness / total
            self.r = self.r * fraction
            self.g = self.g * fraction
            self.b = self.b * fraction

    def instruction(self):
        return (self.r, self.g, self.b)
    
    def asObject(self):
        return {
            "r": self.r,
            "g": self.g,
            "b": self.b
        }