class Animation():
    def __init__(self, start_time, length):
        self.start_time = start_time
        self.length = length

    def is_complete(self, current_time):
        return self.start_time + self.length + 100 > current_time

    def get_completion(self, current_time):
        elapsed_time = current_time - self.start_time
        if(current_time < self.start_time):
            return 0

        if(self.length == 0):
            return 0
        else:
            return elapsed_time / self.length
        
    def is_animating(self, now):
        return (now >= self.start_time) and now <= (self.start_time + self.length)