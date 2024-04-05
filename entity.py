import pygame
import settings
from texture import *
from gameobject import *
from timer import *

class Entity(GameObject):
    def __init__(self, spawn_x, spawn_y, w, h):
        super().__init__(position=Vector2(spawn_x, spawn_y), scale=Vector2(w,h))
        self.velocity = Vector2(4, 4)
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

    def movement(self) -> Vector2:
        pressed_key = pygame.key.get_pressed()

        if pressed_key[pygame.K_SPACE] and not self.is_jumping:
            self.can_jump = True
            self.is_jumping = True
        
        if self.can_jump:
            if self.jump_count >= 0:
                self.transform.position.y -= (self.jump_count * abs(self.jump_count)) * 0.1
                self.jump_count -= 1
            else:
                # This will execute if our jump is finished
                self.jump_count = 20
                self.can_jump = False
                self.is_jumping = False

        movement = Vector2((pressed_key[pygame.K_RIGHT] - pressed_key[pygame.K_LEFT]) * self.velocity.x, (pressed_key[pygame.K_SPACE] * self.velocity.y) + 5)

        self.transform.position.x += movement.x
        self.transform.position.y += movement.y
        
        return movement

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
        
        self.position = self.transform.position
        if self.position.distance(player.transform.position) < self.maximum_distance:
            if self.transform.position.x > self.transform.position.x:
                self.transform.position.x += 1
                self.IsFacingRight = True
            if self.transform.position.x < self.transform.position.x:
                self.transform.position.x -= 1
                self.IsFacingRight = False
       

           
    def update(self, dt):

        self.shoot_timer.update(dt)

        if self.hammer != None:
            self.hammer.transform.position.x += self.Vecteur_directeur.x * self.ThrowSpeed * dt
            self.hammer.transform.position.y += self.Vecteur_directeur.y * self.ThrowSpeed * dt

    def enableThrow(self):
        print("OK")
        self.CanThrow = True

    def tryThrow(self, player: Player):
        if self.CanThrow == False:
            return

        if self.maximum_distance < self.position.distance(player.transform.position) < self.maximum_throw_distance:
            self.hammer = GameObject(position=self.position, scale=Vector2(40, 80))
            self.Vecteur_directeur = Vector2(player.transform.position.x - self.transform.position.x, player.transform.position.y - self.transform.position.y)
            self.Vecteur_directeur.normalize()
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
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_LEFT).draw(pygame.time.get_ticks(),window, self.hammer.transform.position, self.hammer.transform.scale)

        

        
