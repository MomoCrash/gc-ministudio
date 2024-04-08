import pygame
from vector import Vector2
from gameobject import GameObject


class Map:
    def __init__(self, game, map_w, map_h):
        self.width = map_w
        self.height = map_h
        self.elements: list[ GameObject ] = []
        
    def createObject( self, position: Vector2, scale: Vector2 ) -> None:
        self.elements.append( GameObject( position=position, scale=scale, color=pygame.Color( 0, 0, 0 ) ) )
        
    def draw( self, surface: pygame.Surface ) -> None:
        for element in self.elements:
            element.draw( surface )
