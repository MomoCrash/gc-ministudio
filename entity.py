import pygame
from linkedlist import LinkedList
from vector import Vector2
from gameobject import GameObject
from thetimer import Timer
from texture import Sprite, SpriteSheet, Assets, SpriteSheetsRef, SpritesRef
from math import cos, sin, pi



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
                    maxSpeed: float = 4,
                    jumpHeight: float = 1,
                    gravity: float = 5
                ):
        super().__init__( position, rotation, scale, sprite, spriteSheet, spriteDimensions, isVisible, velocity )
        self.maxSpeed: float = maxSpeed
        self.jumpHeight: float = jumpHeight
        self.gravity: float = gravity
        self.isJumping: bool = False
        self.jumpCount: int = 10
        self.isFacingRight = False
        self.CanShoot = True
        self.shoot_timer = Timer(1, self.enableThrow )
        self.ArrowSpeed = 500
        self.arrow: GameObject = None
        self.Vecteur_directeur = Vector2(0,0)
        self.ArrowDistance = 400
        self.circle = pi / self.ArrowDistance


    def update( self, surface: pygame.Surface, mapElements: list[ GameObject ]) -> None:
        pressedKey = pygame.key.get_pressed()
        self.playerMovement( pressedKey, mapElements )
        self.playerJump( pressedKey, mapElements )
        
        self.transform.position.addToSelf( self.velocity )
        self.draw( surface )
        
       

    def UpdateArrow(self, dt):
        if self.arrow != None:
            total_distance_x = abs(self.arrow.transform.position.x - self.startpos)
            
            if total_distance_x >= self.ArrowDistance:
                self.arrow = None
                self.enableThrow()
                return

            self.arrow.transform.position.x += self.Vecteur_directeur.x * self.ArrowSpeed * dt
            self.arrow.transform.position.y -= (cos((total_distance_x / self.ArrowDistance) * pi)*7)
          
    def playerMovement( self, pressedKey: pygame.key.ScancodeWrapper, mapElements: list[ GameObject ] ) -> None:
        leftPressed: bool = pressedKey[ pygame.K_q ]
        rightPressed: bool = pressedKey[ pygame.K_d ]
        
        if ( leftPressed and not rightPressed ):
            
            if ( self.velocity.x == 0 ):
                self.velocity.x = -1
            
            if ( self.velocity.x > 0 ):
                factor: float = 0.6
            else:
                factor: float = 1.5

        elif ( rightPressed and not leftPressed ):
            
            if ( self.velocity.x == 0 ):
                self.velocity.x = 1
            
            if ( self.velocity.x < 0 ):
                factor: float = 0.6
            else:
                factor: float = 1.5
        
        else:
            factor: float = 0.8
        
        if ( abs( self.velocity.x * factor ) <= self.maxSpeed and self.velocity.x != 0 ):
            self.velocity.x *= factor if abs( self.velocity.x ) > 0.9 else 0
        
        self.transform.position.x += self.velocity.x
        collision: bool = False
        for mapObject in mapElements: collision = collision or self.getCollision( mapObject )
        self.transform.position.x -= self.velocity.x
        if ( collision ) : self.velocity.x = 0
    
    def playerJump( self, pressedKey: pygame.key.ScancodeWrapper, mapElements: list[ GameObject ] ):
        spacePressed = pressedKey[ pygame.K_SPACE ]
        
        self.velocity.y = ( spacePressed * self.jumpHeight ) + self.gravity
        
        if ( spacePressed and not self.isJumping ):
            self.isJumping = True
        
        if ( self.isJumping ):
            if ( self.jumpCount >= 0 ):
                self.velocity.y -= ( self.jumpCount * abs( self.jumpCount ) ) * 0.1
                self.jumpCount -= 1
            else:
                # This will execute if our jump is finished
                self.jumpCount = 20
                self.isJumping = False
        
        self.transform.position.y += self.velocity.y
        collision: bool = False
        for mapObject in mapElements: collision = collision or self.getCollision( mapObject )
        self.transform.position.y -= self.velocity.y
        if ( collision ) : self.velocity.y = 0
    
    def is_flip(self):
        pressedKey = pygame.key.get_pressed()
        if pressedKey[pygame.K_d] - pressedKey[pygame.K_q] < 0 and self.isFacingRight:
            self.isFacingRight = False
        elif pressedKey[pygame.K_d] - pressedKey[pygame.K_q] > 0 and not self.isFacingRight:
            self.isFacingRight = True

    def Attack(self):
        print("left click")
        if self.CanShoot:
            self.MousePos = pygame.mouse.get_pos()
            self.arrow = GameObject(position=Vector2(self.transform.position.x, self.transform.position.y))
            #self.Vecteur_directeur = Vector2(self.MousePos[0] - self.transform.position.x, self.MousePos[1] - self.transform.position.y)
            if self.isFacingRight:
                self.Vecteur_directeur = Vector2(1,0.5)
            else:
                self.Vecteur_directeur = Vector2(-1,0.5)


            self.Vecteur_directeur.normalizeToSelf()
            self.CanShoot = False
            self.shoot_timer.start()
            self.startpos = self.arrow.transform.position.x
        
    def enableThrow(self):
        self.CanShoot = True

    def DrawArrow(self,window):
        if self.arrow != None:
            Assets.GetSprite(SpritesRef.TOMAHAWK).draw(window,self.arrow.transform.position,self.arrow.transform.scale)




class Mob( Entity ):
    
    def __init__(
                    self,
                    
                    position: Vector2 = Vector2( 0, 0 ), #? Vector2( 500, 500 )
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    sprite: Sprite = None,
                    spriteSheet: SpriteSheet = None,
                    spriteDimensions: Vector2 = Vector2( 0, 0 ),
                    isVisible: bool = True,
                    
                    velocity: Vector2 = Vector2( 0, 0 ), #? Vector2( 3, 3 )
                    
                    isOnLoop: bool = False,
                    pathPositions: LinkedList = None
                ):
        super().__init__( position, rotation, scale, sprite, spriteSheet, spriteDimensions, isVisible, velocity )
        self.isOnLoop: bool = isOnLoop
        if ( self.isOnLoop ): self.pathDestination: LinkedList = pathPositions.first
        
        self.maximum_distance = 400
        self.maximum_throw_distance = 700
        self.CanThrow = True
        self.ThrowSpeed = 200
        self.WalkSpeed = 100
        self.Vecteur_directeur = Vector2(0,0)
        self.hammer = None
        self.shoot_timer = Timer(3, self.enableThrow )
        self.isFacingRight = False

    def movement( self, player: Player, dt ):
        #running to player
        if self.transform.position.distanceTo( player.transform.position ) < self.maximum_distance:
            if player.transform.position.x > self.transform.position.x:
                self.transform.position.x += self.WalkSpeed * dt
                self.isFacingRight = True
            if player.transform.position.x < self.transform.position.x:
                self.transform.position.x -= self.WalkSpeed * dt
                self.isFacingRight = False

           
    def update(self, dt):
        self.shoot_timer.update(dt)

        if self.hammer != None:
            self.hammer.transform.position.x += self.Vecteur_directeur.x * self.ThrowSpeed * dt
            self.hammer.transform.position.y += self.Vecteur_directeur.y * self.ThrowSpeed * dt

    def enableThrow(self):
        self.CanThrow = True

    def tryThrow( self, player: Player ):
        if self.CanThrow == False:
            return

        if self.maximum_distance < self.transform.position.distanceTo( player.transform.position ) < self.maximum_throw_distance:
            self.hammer = GameObject(position=Vector2(self.transform.position.x, self.transform.position.y))
            self.Vecteur_directeur = Vector2(player.transform.position.x - self.transform.position.x, player.transform.position.y - self.transform.position.y)
            self.Vecteur_directeur.normalizeToSelf()
            self.CanThrow = False
            self.shoot_timer.start()

    def rotate(image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)

    def draw(self, window: pygame.Surface, player: Player):
        #pygame.draw.line(window, (255,255,255), (self.transform.position.x + self.transform.scale.x // 2 ,self.transform.position.y + self.transform.scale.y // 2), (self.Vecteur_directeur.x * self.maximum_throw_distance + player.transform.scale.x // 2  , self.Vecteur_directeur.y * self.maximum_throw_distance  + player.transform.scale.y // 2), 1)
        if self.hammer != None:
            Assets.GetSprite(SpritesRef.TOMAHAWK).draw(window,self.hammer.transform.position,self.hammer.transform.scale)

        

        
