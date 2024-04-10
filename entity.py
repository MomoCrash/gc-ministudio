import pygame
from linkedlist import LinkedList
from vector import Vector2
from gameobject import GameObject
from thetimer import Timer
from texture import Sprite, SpriteSheet, Assets, SpritesRef, SpriteSheetsRef
from math import cos, pi



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
                    isVisible: bool = True,
                    
                    velocity: Vector2 = Vector2( 0, 0 )
                ):
        super().__init__( position, rotation, scale, spriteDimensions, spriteRef, spriteSheetRef, color, isVisible )
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
                    idleSpriteSheet: SpriteSheetsRef = None,
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),
                    isVisible: bool = True,
                    
                    velocity: Vector2 = Vector2( 0, 0 ), #? Vector2( 4, 4 )
                    maxSpeed: float = 4,
                    jumpHeight: float = 50,
                    gravity: float = 10
                ):
        super().__init__( position, rotation, scale, spriteDimensions, None, walkingRightSpriteSheetRef, color, isVisible, velocity )
        self.spriteRenderer.walkingLeftSpriteSheet = walkingLeftSpriteSheetRef
        self.spriteRenderer.walkingRightSpriteSheet = walkingRightSpriteSheetRef
        self.spriteRenderer.idleSpriteSheet = idleSpriteSheet
        self.maxSpeed: float = maxSpeed
        self.jumpHeight: float = jumpHeight
        self.gravity: float = gravity
        self.isJumping: bool = False
        self.jumpCount: int = 10
        self.CanShoot = True
        self.shoot_timer = Timer(1, self.enableThrow )
        self.ArrowSpeed = 500
        self.arrow: GameObject = None
        self.Vecteur_directeur = Vector2(0,0)
        self.ArrowDistance = 400
        self.circle = pi / self.ArrowDistance
    
    def update( self, surface: pygame.Surface, camera: Vector2, solidElements: list[ GameObject ] ) -> None:
        pressedKey = pygame.key.get_pressed()
        self.playerMovement( pressedKey, solidElements )
        self.playerJump( pressedKey, solidElements )
        
        self.transform.position += self.velocity
        
        if ( self.velocity.x < 0 ):
            if ( self.spriteRenderer.spriteSheetRef != self.spriteRenderer.walkingLeftSpriteSheet ):
                self.spriteRenderer.spriteSheetRef = self.spriteRenderer.walkingLeftSpriteSheet
        elif ( self.velocity.x > 0 ):
            if ( self.spriteRenderer.spriteSheetRef != self.spriteRenderer.walkingRightSpriteSheet ):
                self.spriteRenderer.spriteSheetRef = self.spriteRenderer.walkingRightSpriteSheet
        # else:
        #     if ( self.spriteRenderer.spriteSheetRef != self.spriteRenderer.idleSpriteSheet ):
        #         self.spriteRenderer.spriteSheetRef = self.spriteRenderer.idleSpriteSheet

        self.spriteRenderer.draw( surface, camera, self.transform )
    
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
        
        collision: bool = False
        self.transform.position.x += self.velocity.x
        for mapObject in solidElements: collision = collision or self.getCollision( mapObject )
        self.transform.position.x -= self.velocity.x
        if ( collision ) : self.velocity.x = 0
    
    def playerJump( self, pressedKey: pygame.key.ScancodeWrapper, solidElements: list[ GameObject ] ):
        spacePressed = pressedKey[ pygame.K_SPACE ]
        
        if ( spacePressed and not self.isJumping ):
            self.isJumping = True
            self.velocity.y = -self.jumpHeight
        
        if ( self.isJumping ):
            if ( self.velocity.y < -5 ):
                self.velocity.y *= 0.8
            else:
                if ( self.velocity.y < 0 ):
                    self.velocity.y = 1
                if ( self.velocity.y < self.gravity ):
                    self.velocity.y *= 1.5
        
        else:
            self.velocity.y = self.gravity
        
        print
        
        collision: bool = False
        self.transform.position.y += self.velocity.y
        for mapObject in solidElements: collision = collision or self.getCollision( mapObject )
        self.transform.position.y -= self.velocity.y
        if ( collision ) :
            self.velocity.y = 0
            self.isJumping = False

    def Attack(self):
        if self.CanShoot:
            self.MousePos = pygame.mouse.get_pos()
            self.arrow = GameObject(position=Vector2(self.transform.position.x, self.transform.position.y))
            self.Vecteur_directeur = Vector2(self.MousePos[0] - self.transform.position.x, self.MousePos[1] - self.transform.position.y)
            """
            if self.isFacingRight:
                self.Vecteur_directeur = Vector2(1,0.5)
            else:
                self.Vecteur_directeur = Vector2(-1,0.5)
                """


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
                    
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    walkingLeftSpriteSheetRef: SpriteSheetsRef = None,
                    walkingRightSpriteSheetRef: SpriteSheetsRef = None,
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),
                    isVisible: bool = True,
                    
                    velocity: Vector2 = Vector2( 0, 0 ), #? Vector2( 3, 3 )
                    
                    isOnLoop: bool = False,
                    pathPositions: LinkedList = None
                ):
        super().__init__( position, rotation, scale, spriteDimensions, sprite, spriteSheet, color, isVisible, velocity )
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
        self.WalkSpeed = 100

    def movement( self, player: Player, dt ):
        if self.transform.position.distanceTo( player.transform.position ) < self.maximum_distance:
            if player.transform.position.x > self.transform.position.x:
                self.transform.position.x += self.WalkSpeed * dt
                self.isFacingRight = True
            if player.transform.position.x < self.transform.position.x:
                self.transform.position.x -= self.WalkSpeed * dt
                self.isFacingRight = False


           
    def update(self, dt,  surface: pygame.Surface, camera: Vector2, mapElements: list[ GameObject ] ):

        self.shoot_timer.update(dt)

        if self.hammer != None:
            self.hammer.transform.position.x += self.Vecteur_directeur.x * self.ThrowSpeed * dt
            self.hammer.transform.position.y += self.Vecteur_directeur.y * self.ThrowSpeed * dt
        
        
        if ( self.velocity.x < 0 and self.spriteRenderer.spriteSheetRef != self.spriteRenderer.walkingLeftSpriteSheet ): self.spriteRenderer.spriteSheetRef = self.spriteRenderer.walkingLeftSpriteSheet
        elif ( self.velocity.x > 0 and self.spriteRenderer.spriteSheetRef != self.spriteRenderer.walkingRightSpriteSheet ): self.spriteRenderer.spriteSheetRef = self.spriteRenderer.walkingRightSpriteSheet
        self.spriteRenderer.draw( surface, camera, self.transform )

    def enableThrow(self):
        self.CanThrow = True

    def tryThrow( self, player: Player ):
        if self.CanThrow == False:
            return

        if self.maximum_distance < self.transform.position.distanceTo( player.transform.position ) < self.maximum_throw_distance:
            self.hammer = GameObject(position=Vector2(self.transform.position.x,self.transform.position.y))
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
            Assets.GetSprite(SpritesRef.TOMAHAWK).draw(window,self.hammer.transform.position,self.hammer.transform.scale)
        

        
