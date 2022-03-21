class Logger():
    def __init__(self):
        self._DEBUG = False

    def enable(self):
        self._DEBUG = True

    def log(self, message):
        if self._DEBUG:
            print("Log:", message)

    def warn(self, message):
        try:
            f = open("error.log",'a')
            f.write(message)
            f.close()
        except:
            pass
        finally:
            print("Warn:", message)

logger = Logger()