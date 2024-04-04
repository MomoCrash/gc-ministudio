from dataclasses import dataclass
import pygame

from player import *



class Game:
    
    def __init__( self, p_width: int, p_height: int, p_title: str, p_fps: int = 60 ):
        self.width = p_width
        self.height = p_height
        self.title = p_title
        self.fps = p_fps
        
        pygame.init()
        self.screen = pygame.display.set_mode( ( self.width, self.height ) )
        self.surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        
        self.player = Player( 100, 100, 40, 80 )
        self.camera = pygame.Vector2( 0, 0 )
        
        # self.background_sprites = [Assets.GetSprite(SpritesRef.BACKGROUND_0),Assets.GetSprite(SpritesRef.BACKGROUND_0)]
        
        self.loop()
    
    def loop( self ):
        pass