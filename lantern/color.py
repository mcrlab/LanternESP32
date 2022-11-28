def HexColor(hex):
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    return (r, g, b)

def to_hex(color):
        return '{:02x}{:02x}{:02x}'.format( color[0], color[1] , color[2] )