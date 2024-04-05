import pygame
from texture import *
from gameobject import *



class Entity( GameObject ):
    
    def __init__(
                    self,
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    direction: int = -1, # -1 = Left, 1 = Right
                    velocity: Vector2 = Vector2( 0, 0 ),
                    maxVelocity: int = 10,
                    isOnLoop: bool = False,
                    # pathParts: 
                    sprite: Sprite = None,
                    spriteSheet: SpriteSheet = None,
                    isVisible: bool = True
                ):
        super().__init__( position, rotation, scale, sprite, spriteSheet, isVisible )
        self.velocity = velocity
        self.maxVelocity = maxVelocity
        self.direction = direction
        self.isOnLoop = isOnLoop
    
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

class Mob(Entity):
    pass