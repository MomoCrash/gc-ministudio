import pygame


class Game:
    def __init__(self, win_width, win_height, win_name, fps=60):
        self.width = win_width
        self.height = win_height
        self.window_name = win_name
        self.fps = fps

        self.loop()

    def inputs(self):
        pass

    def update_graphics(self):
        pass

    def loop(self):
        while True:
            break
