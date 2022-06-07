
from math import ceil


def test(percentage, interval):
    fps = (1000 / interval)
    
    print(ceil(percentage * fps) / fps)

for i in range(0, 100):
    a = i / 100
    test(a, 62.5)
    #test(0.55, 50)