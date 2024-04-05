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
        self.map.create_object(0, 850, 3000, 20)
        self.map.create_object(1000, 900, 200, 80)
        self.map.create_object(1500, 650, 250, 80)
        self.map.create_object(2500, 650, 250, 80)
        
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.player = Player(100, 100, 40, 80)
        self.camera = pygame.Vector2(0, 0)
        
        self.background_sprites = [Assets.GetSprite(SpritesRef.BACKGROUND_0),Assets.GetSprite(SpritesRef.BACKGROUND_0)]

        self.loop()

    def inputs(self) -> bool:

        self.player.movement()
        self.player.is_flip()

        self.camera.x = self.player.rect_transform.x - self.width // 4
        self.camera.y = self.player.rect_transform.y - self.height // 4

        self.camera.x = max(0, min(self.camera.x, self.width))
        self.camera.y = max(0, min(self.camera.y, self.height))
        
        for mapObject in self.map.elements:
            mapObject.rect_transform.x = mapObject.position.x - self.camera.x

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False
        return True

    def update_graphics(self):

        self.map.draw(self.surface)

        for i, segment in enumerate(self.background_sprites):
            self.surface.blit(segment.texture, (i * self.width - self.camera.x, 0))
       
        # Draw the player flipped on the good side
        if self.player.IsFacingRight:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_RIGHT).draw(pygame.time.get_ticks(), self.surface, self.player.rect_transform)
        else:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_LEFT).draw(pygame.time.get_ticks(), self.surface, self.player.rect_transform)

        #for mapObject in self.map.elements:
        #    mapObject.draw(self.surface)

        pygame.display.flip()

    def loop(self):
        running = True
        while running:

            running = self.inputs()

            for mapObject in self.map.elements:
                self.player.check_collision(mapObject.rect_transform)

            self.update_graphics()

            self.clock.tick(60)
            
        pygame.quit()
        
