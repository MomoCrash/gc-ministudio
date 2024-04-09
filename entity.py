import pygame
from linkedlist import LinkedList
from vector import Vector2
from gameobject import GameObject
from thetimer import Timer
from texture import Sprite, SpriteSheet, Assets, SpritesRef, SpriteSheetsRef



class Entity( GameObject ):
    
    def __init__(
                    self,
                    
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    spriteRef: SpritesRef = None,
                    spriteSheetRef: SpriteSheetsRef = None,
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),
                    
                    velocity: Vector2 = Vector2( 0, 0 ) #? Vector2( 4, 4 )
                ):
        super().__init__( position, rotation, scale, spriteDimensions, spriteRef, spriteSheetRef, color )
        self.velocity: Vector2 = velocity
    
    def update( self, surface: pygame.Surface, camera: Vector2, deltaTime: int ) -> None:
        self.transform.position.addToSelf( self.velocity.multiplyToNew( deltaTime ) )
        self.spriteRenderer.draw( surface, camera, self.transform )



class Player( Entity ):
    def __init__(
                    self,
                    
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    walkingLeftSpriteSheetRef: SpriteSheetsRef = None,
                    walkingRightSpriteSheetRef: SpriteSheetsRef = None,
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),
                    
                    velocity: Vector2 = Vector2( 0, 0 ), #? Vector2( 4, 4 )
                    maxSpeed: float = 4,
                    jumpHeight: float = 1,
                    gravity: float = 5
                ):
        super().__init__( position, rotation, scale, spriteDimensions, None, walkingRightSpriteSheetRef, color, velocity )
        self.spriteRenderer.walkingLeftSpriteSheet = walkingLeftSpriteSheetRef
        self.spriteRenderer.walkingRightSpriteSheet = walkingRightSpriteSheetRef
        self.maxSpeed: float = maxSpeed
        self.jumpHeight: float = jumpHeight
        self.gravity: float = gravity
        self.isJumping: bool = False
        self.jumpCount: int = 10
    
    def update( self, surface: pygame.Surface, camera: Vector2, mapElements: list[ GameObject ] ) -> None:
        pressedKey = pygame.key.get_pressed()
        self.playerMovement( pressedKey, mapElements )
        self.playerJump( pressedKey, mapElements )
        
        self.transform.position.addToSelf( self.velocity )
        
        if ( self.velocity.x < 0 and self.spriteRenderer.spriteSheetRef != self.spriteRenderer.walkingLeftSpriteSheet ): self.spriteRenderer.spriteSheetRef = self.spriteRenderer.walkingLeftSpriteSheet
        elif ( self.velocity.x > 0 and self.spriteRenderer.spriteSheetRef != self.spriteRenderer.walkingRightSpriteSheet ): self.spriteRenderer.spriteSheetRef = self.spriteRenderer.walkingRightSpriteSheet
        self.spriteRenderer.draw( surface, camera, self.transform )
    
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
        
        collision: bool = False
        self.transform.position.x += self.velocity.x
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
        
        collision: bool = False
        self.transform.position.y += self.velocity.y
        for mapObject in mapElements: collision = collision or self.getCollision( mapObject )
        self.transform.position.y -= self.velocity.y
        if ( collision ) : self.velocity.y = 0

    def Attack(self):
        print("left click")


class Mob( Entity ):
    
    def __init__(
                    self,
                    
                    position: Vector2 = Vector2( 0, 0 ), #? Vector2( 500, 500 )
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    sprite: SpritesRef = None,
                    spriteSheet: SpriteSheetsRef = None,
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),
                    
                    velocity: Vector2 = Vector2( 0, 0 ), #? Vector2( 3, 3 )
                    
                    isOnLoop: bool = False,
                    pathPositions: LinkedList = None
                ):
        super().__init__( position, rotation, scale, spriteDimensions, sprite, spriteSheet, color, velocity )
        self.isOnLoop: bool = isOnLoop
        if ( self.isOnLoop ): self.pathDestination: LinkedList = pathPositions.first
        
        self.maximum_distance = 400
        self.maximum_throw_distance = 700
        self.CanThrow = True
        self.ThrowSpeed = 200
        self.Vecteur_directeur = pygame.Vector2(0,0)
        self.hammer = None
        self.shoot_timer = Timer(3, self.enableThrow )
        self.isFacingRight = False

    def movement( self, player: Player ):
        
        if self.transform.position.distanceTo( player.transform.position ) < self.maximum_distance:
            if self.transform.position.x > self.transform.position.x:
                self.transform.position.x += 1
                self.isFacingRight = True
            if self.transform.position.x < self.transform.position.x:
                self.transform.position.x -= 1
                self.isFacingRight = False

           
    def update(self, dt):

        self.shoot_timer.update(dt)

        if self.hammer != None:
            self.hammer.transform.position.x += self.Vecteur_directeur.x * self.ThrowSpeed * dt
            self.hammer.transform.position.y += self.Vecteur_directeur.y * self.ThrowSpeed * dt

    def enableThrow(self):
        print("OK")
        self.CanThrow = True

    def tryThrow( self, player: Player ):
        if self.CanThrow == False:
            return

        if self.maximum_distance < self.transform.position.distanceTo( player.transform.position ) < self.maximum_throw_distance:
            self.hammer = GameObject(position=self.transform.position, scale=Vector2(40, 80))
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
        #pygame.draw.line(window, (255,255,255), (self.rect_transform.x + self.width // 2 ,self.rect_transform.y + self.height // 2), (self.Vecteur_directeur.x * self.maximum_throw_distance + player.rect_transform.width // 2  , self.Vecteur_directeur.y * self.maximum_throw_distance  + player.rect_transform.height // 2), 1)
        if self.hammer != None:
            Assets.GetSpriteSheet(SpriteSheetsRef.PLAYER_WALK_LEFT).draw(pygame.time.get_ticks(),window, self.hammer.transform.position, self.hammer.transform.scale)

        

        
