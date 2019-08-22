from color import calculate_color
from color import Color

for now in range(0,20):
    previous_color = Color(255,0,0)
    current_color = Color(255,0,0)
    target_color = Color(0,255,0)
    animation_length = 10
    animation_start_time = 5


    color_to_render = calculate_color(now, animation_length, animation_start_time, previous_color, current_color, target_color)
    print(color_to_render.instruction())