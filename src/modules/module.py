import threading

class Module(threading.Thread):

    def __init__(self):
        self.flag = threading.Event()
    
    @staticmethod
    def validate(self):
        raise NotImplementedError
