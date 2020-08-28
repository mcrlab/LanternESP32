from colr import color
from colr import Colr as C
print(color('Hello there.', fore=(255, 0, 0), back=(0, 0, 0)))
print(color('Hello there.', fore='bada55', back='000'))
print(C().hex('ff0000', 'test', rgb_mode=True))
print(C().rgb(255, 0, 0, 'test'))
