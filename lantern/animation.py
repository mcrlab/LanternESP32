class Animation():
    def __init__(self, start_time, length):
        self.start_time = start_time
        self.length = length

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