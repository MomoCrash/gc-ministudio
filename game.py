import pygame
from map import Map

class Game:
    def __init__(self, win_width, win_height, win_name, fps=60):
        self.width = win_width
        self.height = win_height
        self.window_name = win_name
        self.fps = fps
        self.map = Map(self, win_width, win_height)
        
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.loop()

    def inputs(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    
                    #Test key
                    pass
                    
            if event.type == pygame.QUIT:
                return False
        return True

    def update_graphics(self):
        self.map.draw(self.surface)
        
        pygame.display.flip()

    def loop(self):
        running = True
        while running:

            self.screen.fill("gray")

            running = self.inputs()
            self.update_graphics()

            self.clock.tick(60)
            
        pygame.quit()
        
