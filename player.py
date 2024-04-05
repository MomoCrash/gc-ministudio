import pygame
import settings
from texture import *
from gameobject import GameObject
from timer import *

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

class Mob(Entity):
    def __init__(self, spawn_x, spawn_y, w, h):
        super().__init__(spawn_x, spawn_y, w, h)
        self.x = 500
        self.y = 500
        self.velocity = pygame.Vector2(3,3)
        self.maximum_distance = 400
        self.maximum_throw_distance = 700
        self.CanThrow = True
        self.ThrowSpeed = 200
        self.Vecteur_directeur = pygame.Vector2(0,0)
        self.hammer = None
        self.shoot_timer = Timer(3, self.enableThrow )

    def movement(self, player: Player):
        
        position = pygame.Vector2(self.rect_transform.x,self.rect_transform.y)
        if pygame.Vector2.distance_to(position,pygame.Vector2(player.rect_transform.x, player.rect_transform.y)) < self.maximum_distance:
            if player.rect_transform.x > self.rect_transform.x:
                self.rect_transform.x += 1
                self.IsFacingRight = True
            if player.rect_transform.x < self.rect_transform.x:
                self.rect_transform.x -= 1
                self.IsFacingRight = False
       

           
    def update(self, dt):
        self.position = pygame.Vector2(self.rect_transform.x,self.rect_transform.y)

        self.shoot_timer.update(dt)

        if self.hammer != None:
            self.hammer.rect_transform.x += self.Vecteur_directeur.x * self.ThrowSpeed * dt
            self.hammer.rect_transform.y += self.Vecteur_directeur.y * self.ThrowSpeed * dt

    def enableThrow(self):
        print("OK")
        self.CanThrow = True

    def tryThrow(self, player: Player):
        if self.CanThrow == False:
            return

        if self.maximum_distance < pygame.Vector2.distance_to(self.position,pygame.Vector2(player.rect_transform.x, player.rect_transform.y)) < self.maximum_throw_distance:
            self.hammer = GameObject(self.position, 40, 80)
            self.Vecteur_directeur = pygame.Vector2(player.rect_transform.x - self.rect_transform.x, player.rect_transform.y - self.rect_transform.y)
            self.Vecteur_directeur.normalize_ip()
            self.CanThrow = False
            self.shoot_timer.start()

    def rotate(image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
    

        
        
                
            
        


    def draw(self, window: pygame.Surface, player: Player):
        #pygame.draw.line(window, (255,255,255), (self.rect_transform.x + self.width // 2 ,self.rect_transform.y + self.height // 2), (self.Vecteur_directeur.x * self.maximum_throw_distance + player.rect_transform.width // 2  , self.Vecteur_directeur.y * self.maximum_throw_distance  + player.rect_transform.height // 2), 1)
        if self.hammer != None:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_LEFT).draw(pygame.time.get_ticks(),window, self.hammer.rect_transform)

        

        
