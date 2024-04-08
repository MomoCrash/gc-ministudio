import pygame
from vector import Vector2
from map import Map
from text import Text
from entity import Entity, Player, Mob
from texture import SpritesRef, SpriteSheetsRef, Sprite, SpriteSheet, Assets


class Game:
    def __init__(self, win_width, win_height, win_name, fps=60):
        self.width = win_width
        self.height = win_height
        self.window_name = win_name
        self.fps = fps
        self.dt = 0
        self.current_dt = 0

        self.map = Map( "map1.txt", win_width, win_height )
        self.map.load_map()
        
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.player = Player( position=Vector2( 1000, 500 ), scale=Vector2( 40, 80 ) )
        self.mob = Mob( position=Vector2( 500, 500 ), scale=Vector2( 40, 80 ) )
        self.camera = pygame.Vector2(0, 0)

        self.text = Text(self.screen, "Arial")
        
        self.background_sprites = [Assets.GetSprite(SpritesRef.BACKGROUND_0),Assets.GetSprite(SpritesRef.BACKGROUND_0)]

        self.loop()

    def inputs(self) -> bool:
        
        self.player.update( self.surface, self.map.decors )
        self.player.is_flip()

        self.camera.x = self.player.transform.position.x - self.width // 4
        self.camera.y = self.player.transform.position.y - self.height // 4

        self.camera.x = max(0, min(self.camera.x, self.width))
        self.camera.y = max(0, min(self.camera.y, self.height))

        for mapObject in self.map.decors:
            mapObject.transform.position.x = mapObject.initial_position.x - self.camera.x

        for mapObject in self.map.colliders:
            mapObject.transform.position.x = mapObject.initial_position.x - self.camera.x

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    self.player.Attack()
        return True
    
    
    def update(self):
        pass

    def update_graphics(self):

        for i, segment in enumerate(self.background_sprites):
            self.surface.blit(segment.texture, (i * self.width - self.camera.x, 0))

        self.map.draw(self.screen)
       
        # Draw the player flipped on the good side
        if self.player.isFacingRight:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_RIGHT).draw(pygame.time.get_ticks(), self.surface, self.player.transform.position, self.player.transform.scale)
        else:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_LEFT).draw(pygame.time.get_ticks(), self.surface, self.player.transform.position, self.player.transform.scale)

        if self.mob.isFacingRight:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_RIGHT).draw(pygame.time.get_ticks(), self.surface, self.mob.transform.position, self.mob.transform.scale)
        else:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_LEFT).draw(pygame.time.get_ticks(), self.surface, self.mob.transform.position, self.mob.transform.scale)

        # Develop in progress
        self.mob.movement(self.player)

        self.mob.tryThrow(self.player)
        self.mob.update(self.dt)
        self.mob.draw(self.surface, self.player)

        self.text.draw_text("Test de Text adaptatif !", (255, 255, 255), 100, 100, 10, 10)

        #Assets.GetSprite(SpritesRef.LIGHT).draw(self.surface, (self.camera.x ,self.camera.y))

        

        pygame.display.flip()

    def loop(self):
        running = True
        while running:
            dt_start = pygame.time.get_ticks()

            running = self.inputs()

            self.update_graphics()

            self.clock.tick(60)
            
            dt_end = pygame.time.get_ticks()
            self.dt =self.clock.get_time() / 1000
            self.current_dt += self.dt
        pygame.quit()
        
