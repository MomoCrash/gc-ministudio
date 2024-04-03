import pygame


class GameObject:
    def __init__(self, pos: pygame.Vector2, width, height):
        self.position = pos
        self.width = width
        self.height = height
        
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), pygame.Rect(self.position.x, self.position.y, self.width, self.height))

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