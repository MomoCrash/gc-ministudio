import pygame
import settings
import os


class Sprite:
    def __init__(self, path_to_texture, width, height):
        self.texture_path = path_to_texture
        self.texture = pygame.image.load(path_to_texture)
        self.size = (width, height)
        self.texture = pygame.transform.scale(self.texture, self.size)
        
    def draw(self, surface: pygame.Surface, pos: pygame.Rect):
        surface.blit(self.texture, pos)
        

class SpriteSheet:
    def __init__(self, textures: list[Sprite]):
        self.frame_count = len(textures)
        self.frame_per_image = settings.ANIMATION_DURATION / self.frame_count
        self.textures = textures
        self.current_index = 0
        self.time = pygame.time.get_ticks()
        
    def draw(self, ticks, surface: pygame.Surface, pos: pygame.Rect):
        if self.is_next_frame(ticks):
            self.current_index += 1
            if self.current_index >= self.frame_count:
                self.current_index = 0
        self.textures[self.current_index].draw(surface, pos)
    
    def is_next_frame(self, current_ticks) -> bool:
        if current_ticks - self.time > self.frame_per_image:
            return True
        return False
        
    
class Assets:

    Texture = {}

    @staticmethod
    def Init():

    @staticmethod
    def Get():
        pass