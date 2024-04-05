import pygame
from map import Map
from texture import *
from player import *

class Game:
    def __init__(self, win_width, win_height, win_name, fps=60):
        self.width = win_width
        self.height = win_height
        self.window_name = win_name
        self.fps = fps

        self.map = Map(self, win_width, win_height)
        self.map.create_object(0, 600, 1000, 800)
        
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.player = Player(100, 100, 40, 80)

        self.loop()

    def inputs(self) -> bool:

        self.player.movement()
        self.player.is_flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    self.player.Attack()
        return True

    def update_graphics(self):

        self.map.draw(self.surface)

        if self.player.IsFacingRight:
            Assets.SpriteSheets[SheetsRef.PLAYER_WALK_RIGHT.value - 1].draw(pygame.time.get_ticks(), self.surface, self.player.rect_transform)
        else:
            Assets.SpriteSheets[SheetsRef.PLAYER_WALK_LEFT.value - 1].draw(pygame.time.get_ticks(), self.surface, self.player.rect_transform)


        for mapObject in self.map.elements:
            mapObject.draw(self.surface)

        Assets.Texture[TextureRef.LIGHT.value].draw(self.surface, (self.player.rect_transform.x - Assets.Texture[TextureRef.LIGHT.value].size[0] // 2 + 50 ,self.player.rect_transform.y- Assets.Texture[TextureRef.LIGHT.value].size[1] // 2))


        pygame.display.flip()

    def loop(self):
        running = True
        while running:

            self.screen.fill("gray")

            running = self.inputs()

            for mapObject in self.map.elements:
                self.player.check_collision(mapObject.rect_transform)

            self.update_graphics()

            self.clock.tick(60)
            
        pygame.quit()
        
