import pygame
from vector import Vector2
from gameobject import GameObject
from texture import Sprite, SpriteSheet

class Entity(GameObject):
    def __init__(self, spawn_x, spawn_y, w, h):
        super().__init__(pygame.Vector2(spawn_x, spawn_y), w, h)
        self.velocity = pygame.Vector2(4, 4)
        self.max_velocity = 10
        self.IsFacingRight = False
        self.left = False
        self.right = False
        self.can_jump = False
        self.is_jumping = False
        self.jump_count = 10

    def movement(self):
        pass

    def flip(self):
        pass


class Player(Entity):
    def __init__(self, x, y, w, h) :
        super().__init__(x, y, w, h)
        self.x = 100
        self.y = 100

    def movement(self):
        pressed_key = pygame.key.get_pressed()

        if pressed_key[pygame.K_SPACE] and not self.is_jumping:
            self.can_jump = True
            self.is_jumping = True
        
        if self.can_jump:
            if self.jump_count >= 0:
                self.rect_transform.y -= (self.jump_count * abs(self.jump_count)) * 0.1
                self.jump_count -= 1
            else:
                # This will execute if our jump is finished
                self.jump_count = 20
                self.can_jump = False
                self.is_jumping = False

        self.rect_transform.x += (pressed_key[pygame.K_RIGHT] - pressed_key[pygame.K_LEFT]) * self.velocity.x
        self.rect_transform.y += (pressed_key[pygame.K_SPACE] * self.velocity.y) + 5

    def is_flip(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_RIGHT] - pressed_key[pygame.K_LEFT] < 0 and self.IsFacingRight:
            self.IsFacingRight = False
        elif pressed_key[pygame.K_RIGHT] - pressed_key[pygame.K_LEFT] > 0 and not self.IsFacingRight:
            self.IsFacingRight = True

    def Attack(self):
        print("left click")

