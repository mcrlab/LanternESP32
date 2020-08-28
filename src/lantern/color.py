class Color():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def normalise(self, maximum_brightness):
        total = self.r + self.g + self.b
        if (total > maximum_brightness):
            fraction = maximum_brightness / total
            self.r = int(self.r * fraction)
            self.g = int(self.g * fraction)
            self.b = int(self.b * fraction)

    def instruction(self):
        return (self.r, self.g, self.b)
    
    def as_object(self):
        return {
            "r": self.r,
            "g": self.g,
            "b": self.b
        }
    def as_hex(self):
        return '{:02x}{:02x}{:02x}'.format( self.r, self.g , self.b )