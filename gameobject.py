import pygame


class GameObject:
    def __init__(self, pos: pygame.Vector2, width, height):
        self.position = pos
        self.width = width
        self.height = height
        self.rect_transform = pygame.rect.Rect(self.position.x, self.position.y, width, height)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255),
                         pygame.Rect(self.position.x, self.position.y, self.width, self.height))

    def check_collision(self, other_rect: pygame.Rect):
        collide = pygame.Rect.colliderect(self.rect_transform, other_rect)
        if collide:
            self.rect_transform.bottom = other_rect.top
