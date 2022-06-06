from .easing import easings
from .easing import ElasticEaseOut as default_easing
class Animation():
    def __init__(self, start_time, length, easing):
        self.start_time = start_time
        self.length = length
        self.easing = easing

        if easing in easings:
            self.easing_fn =  easings[easing]
        else:
            self.easing_fn = default_easing

    def get_completion(self, current_time):
        elapsed_time = current_time - self.start_time
        if(current_time < self.start_time):
            return 0
        if current_time >= self.start_time + self.length:
            return 1
        if(self.length == 0):
            return 0
        else:
            return elapsed_time / self.length