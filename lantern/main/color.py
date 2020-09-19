def test(color):
    if(color < 0):
        return 0
    elif(color > 255):
        return 255
    else:
        return color


class Color():
    def __init__(self, r, g, b):
        self.r = test(int(r))
        self.g = test(int(g))
        self.b = test(int(b))
        

    def normalise(self, maximum_brightness):
        total = self.r + self.g + self.b
        if (total > maximum_brightness):
            fraction = maximum_brightness / total
            self.r = int(self.r * fraction)
            self.g = int(self.g * fraction)
            self.b = int(self.b * fraction)

    def as_instruction(self):
        return (self.r, self.g, self.b)
    
    def as_object(self):
        return {
            "r": self.r,
            "g": self.g,
            "b": self.b
        }
    def as_hex(self):
        return '#{:02x}{:02x}{:02x}'.format( self.r, self.g , self.b )