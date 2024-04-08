
class Timer():
    def __init__(self, delay, callback):
        self.delay = delay
        self.elapsed = 0
        self.is_active = False
        self.callback = callback

    def update(self, dt):
        if self.is_active == False:
            return
        
        self.elapsed += dt

        if self.elapsed >= self.delay:
            self.is_active = False
            self.callback()


    def start(self):
        self.elapsed = 0
        self.is_active = True

        






        