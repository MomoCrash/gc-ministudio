import pygame


class GameObject:
    def __init__(self, pos: pygame.Vector2, width, height):
        self.position = pos
        self.width = width
        self.height = height
        self.rect_transform = pygame.Rect(self.position.x, self.position.y, width, height)

    def draw(self, surface: pygame.Surface, color: pygame.Color):
        pass

    def check_collision(self, other_rect: pygame.Rect):
        
        collide = pygame.Rect.colliderect(self.rect_transform, other_rect)
        if collide:
            self.rect_transform.bottom = other_rect.top


class SolidObject(GameObject):
    def __init__(self, pos: pygame.Vector2, width, height):
        super().__init__(pos, width, height)
        
    def draw(self, surface: pygame.Surface, color: pygame.Color):
        pygame.draw.rect(surface, color,
                         pygame.Rect(self.rect_transform.x, self.rect_transform.y, self.width, self.height))

        
class ColliderObject(GameObject):
    def __init__(self, pos: pygame.Vector2, width, height):
        super().__init__(pos, width, height)