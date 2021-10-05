class Logger():
    def __init__(self):
        self.DEBUG = False

    def log(self, message):
        if self.DEBUG:
            print("Log:", message)

    def warn(self, message):
        print("Warn:", message)

logger = Logger()