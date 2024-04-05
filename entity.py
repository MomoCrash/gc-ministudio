import pygame
from linkedlist import LinkedList
from vector import Vector2
from gameobject import GameObject
from texture import Sprite, SpriteSheet, Assets, SpriteSheetsRef



class Entity( GameObject ):
    
    def __init__(
                    self,
                    
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    sprite: Sprite = None,
                    spriteSheet: SpriteSheet = None,
                    spriteDimensions: Vector2 = Vector2( 0, 0 ),
                    isVisible: bool = True,
                    
                    velocity: Vector2 = Vector2( 0, 0 ) #? Vector2( 4, 4 )
                ):
        super().__init__( position, rotation, scale, sprite, spriteSheet, spriteDimensions, isVisible )
        self.velocity: Vector2 = velocity
    
    def update( self, surface: pygame.Surface, deltaTime: int ) -> None:
        self.transform.position.addToSelf( self.velocity.multiplyToNew( deltaTime ) )
        self.draw( surface )



class Player( Entity ):
    def __init__(
                    self,
                    
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    sprite: Sprite = None,
                    spriteSheet: SpriteSheet = None,
                    spriteDimensions: Vector2 = Vector2( 0, 0 ),
                    isVisible: bool = True,
                    
                    velocity: Vector2 = Vector2( 0, 0 ), #? Vector2( 4, 4 )
                    maxSpeed: float = 1
                ):
        super().__init__( position, rotation, scale, sprite, spriteSheet, spriteDimensions, isVisible, velocity )
        self.maxSpeed: float = maxSpeed
        self.isJumping: bool = False
        self.isFacingRight = True #! To Remove
    
    def update( self, surface: pygame.Surface, deltaTime: int ) -> None:
        self.movement()
        self.transform.position.addToSelf( self.velocity.multiplyToNew( deltaTime ) )
        self.draw( surface )
    
    def movement( self ) -> Vector2:
        pressed_key = pygame.key.get_pressed()
        
        if ( pressed_key[ pygame.K_SPACE ] and not self.isJumping ):
            self.isJumping = True
        
        if ( self.isJumping ):
            if ( self.JumpCount >= 0 ):
                self.transform.position.y -= ( self.JumpCount * abs( self.JumpCount ) ) * 0.1
                self.JumpCount -= 1
            else:
                # This will execute if our jump is finished
                self.JumpCount = 20
                self.isJumping = False
        
        movement = Vector2( ( pressed_key[ pygame.K_RIGHT ] - pressed_key[ pygame.K_LEFT ] ) * self.velocity.x, ( pressed_key[ pygame.K_SPACE ] * self.velocity.y ) + 5 )
        self.transform.position.addToSelf( movement )
        return movement
    
    def is_flip(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_RIGHT] - pressed_key[pygame.K_LEFT] < 0 and self.IsFacingRight:
            self.IsFacingRight = False
        elif pressed_key[pygame.K_RIGHT] - pressed_key[pygame.K_LEFT] > 0 and not self.IsFacingRight:
            self.IsFacingRight = True

    def Attack(self):
        print("left click")



class Mob( Entity ):
    
    def __init__(
                    self,
                    
                    position: Vector2 = Vector2( 0, 0 ), #? Vector2( 500, 500 )
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    sprite: Sprite = None,
                    spriteSheet: SpriteSheet = None,
                    isVisible: bool = True,
                    
                    velocity: Vector2 = Vector2( 0, 0 ), #? Vector2( 3, 3 )
                    
                    isOnLoop: bool = False,
                    pathPositions: LinkedList = None
                ):
        super().__init__( position, rotation, scale, sprite, spriteSheet, isVisible, velocity )
        self.isOnLoop: bool = isOnLoop
        if ( self.isOnLoop ): self.pathDestination: LinkedList = pathPositions.first
        
        
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

        

        
