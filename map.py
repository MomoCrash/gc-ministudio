import pygame
from gameobject import GameObject


class Map:
    def __init__(self, game, map_w, map_h):
        self.width = map_w
        self.height = map_h
        self.elements: list[GameObject] = []
        
    def create_object(self, x, y, w, h):
        self.elements.append(GameObject(pygame.Vector2(x, y), w, h))
        
    def draw(self, surface: pygame.Surface):
        for element in self.elements:
            element.draw(surface)
