from __future__ import annotations
import pygame
from linkedlist import LinkedList
from vector import Vector2
from gameobject import GameObject
from thetimer import Timer
from texture import Sprite, SpriteSheet, Assets, SpritesRef, SpriteSheetsRef
from math import  pi




class Entity( GameObject ):
    
    def __init__(
                    self,
                    
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),

                    spritesheet_ref: SpriteSheetsRef = SpriteSheetsRef.ENNEMY_WALK_RIGHT,
                    
                    velocity: Vector2 = Vector2( 0, 0 )
                ):
        super().__init__( position, rotation, scale, spriteDimensions, None, spritesheet_ref, color )
        self.velocity: Vector2 = velocity
    
    def update( self, surface: pygame.Surface, camera: Vector2, deltaTime: int ) -> None:
        self.transform.position += self.velocity * deltaTime
        self.spriteRenderer.draw( surface, camera, self.transform )



class Player( Entity ):
    def __init__(
                    self,
                    
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    spritesheet_ref: SpriteSheetsRef = SpriteSheetsRef.PLAYER_WALK_LEFT,
                    
                    velocity: Vector2 = Vector2( 0, 0 ), #? Vector2( 4, 4 )
                    maxSpeed: float = 4,
                    jumpHeight: float = 50,
                    gravity: float = 10
                ):
        super().__init__( position, rotation, scale, spriteDimensions, None, spritesheet_ref, velocity )
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
        self.ArrowDistance = 500
        self.circle = pi / self.ArrowDistance
        self.health = 10
        self.isHit = False
        self.shield = False
        self.CanAttack = True
        self.AttackRange = 70
        self.isAttacking = False
        self.timer_between_attack = Timer(1, self.enableMeleeAttack)

    def FinishAnim(self):
        self.isHit = False
        self.isAttacking = False

    def enableMeleeAttack(self):
        self.CanAttack = True

    def MeleeAttack(self):
        if self.CanAttack == False:
            return
        else:
            self.isAttacking = True
            self.CanAttack = False
            self.timer_between_attack.start()
    
    def update( self, surface: pygame.Surface, camera: Vector2, solidElements: list[ GameObject ],dt ) -> None:
        pressedKey = pygame.key.get_pressed()
        self.playerMovement( pressedKey, solidElements )
        self.playerJump( pressedKey, solidElements )
        self.timer_between_attack.update(dt)
        

        self.transform.position += self.velocity
        
        if self.velocity.x < 0: 
            if self.isHit:
                  self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.PLAYER_GET_HIT_LEFT
            elif self.shield:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.PLAYER_SHIELD_LEFT
            elif self.isAttacking:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.PLAYER_ATTACK_LEFT
            else:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.PLAYER_WALK_LEFT
        else:
            if self.isHit:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.PLAYER_GET_HIT_RIGHT  
            elif self.shield:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.PLAYER_SHIELD_RIGHT
            elif self.isAttacking:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.PLAYER_ATTACK_RIGHT
            else:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.PLAYER_WALK_RIGHT

        self.spriteRenderer.draw( surface, camera, self.transform, self.FinishAnim )

    
    def UpdateArrow(self, dt):
        if self.arrow != None:
            total_distance_x = abs(self.arrow.transform.position.x - self.startpos)
            
            if total_distance_x >= self.ArrowDistance:
                self.arrow = None
                self.enableThrow()
                return

            self.arrow.transform.position.x += self.Vecteur_directeur.x * self.ArrowSpeed * dt
            self.arrow.transform.position.y +=  self.Vecteur_directeur.y * self.ArrowSpeed * dt

    def DamageEnnemy(self, mob: Mob):
        if self.arrow != None:
            if self.arrow.getCollision(mob) and mob.shield == False:
                print("b")
                mob.isHit = True
                self.arrow = None
                self.enableThrow()
                return
            if self.arrow.getCollision(mob) and mob.shield:
                print("c")
                self.arrow = None
                mob.shield = False
                self.enableThrow()
                return
            """
        self.transform.anchor = (0.5,0.5)
        mob.transform.anchor = (0.5,0.5)
        if self.transform.position.x + (self.GetWidth() if self.velocity.x > 0 else -self.GetWidth()) == mob.transform.position.x + (mob.GetWidth() if mob.velocity.x > 0 else -mob.GetWidth()):
            """

    def playerMovement(self, pressedKey: pygame.key.ScancodeWrapper, solidElements: list[GameObject]) -> None:
        leftPressed: bool = pressedKey[pygame.K_q]
        rightPressed: bool = pressedKey[pygame.K_d]

        if (leftPressed and not rightPressed):

            if (self.velocity.x == 0):
                self.velocity.x = -1

            if (self.velocity.x > 0):
                factor: float = 0.6
            else:
                factor: float = 1.5

        elif (rightPressed and not leftPressed):

            if (self.velocity.x == 0):
                self.velocity.x = 1

            if (self.velocity.x < 0):
                factor: float = 0.6
            else:
                factor: float = 1.5

        else:
            factor: float = 0.8

        if (abs(self.velocity.x * factor) <= self.maxSpeed and self.velocity.x != 0):
            self.velocity.x *= factor if abs(self.velocity.x) > 0.9 else 0

        collision: bool = False
        self.transform.position.x += self.velocity.x
        for mapObject in solidElements: collision = collision or self.getCollision(mapObject)
        self.transform.position.x -= self.velocity.x
        if (collision): self.velocity.x = 0

    def playerJump(self, pressedKey: pygame.key.ScancodeWrapper, solidElements: list[GameObject]):
        spacePressed = pressedKey[pygame.K_SPACE]


        if (spacePressed and not self.isJumping):
            self.isJumping = True
            self.velocity.y = -self.jumpHeight

        if (self.isJumping):
            if (self.velocity.y < -5):
                self.velocity.y *= 0.8

            else:
                if (self.velocity.y < 0):
                    self.velocity.y = 1
                if (self.velocity.y < self.gravity):
                    self.velocity.y *= 1.5

        else:
            self.velocity.y = self.gravity
        
        collision: bool = False
        self.transform.position.y += self.velocity.y
        for mapObject in solidElements: collision = collision or self.getCollision( mapObject )
        self.transform.position.y -= self.velocity.y
        if ( collision ) :
            self.velocity.y = 0
            self.isJumping = False

    def Attack(self, camera: Vector2):
        if self.CanShoot:
            self.MousePos = pygame.mouse.get_pos()
            self.arrow = GameObject(position=Vector2(self.transform.position.x, self.transform.position.y), spriteRef=SpritesRef.TOMAHAWK)#, anchor=Vector2(0.5, 0.5))
            self.Vecteur_directeur = Vector2(self.MousePos[0] - self.transform.position.x + camera.x, self.MousePos[1] - self.transform.position.y + camera.y)
            self.Vecteur_directeur.normalizeToSelf()
            self.CanShoot = False
            self.shoot_timer.start()
            self.startpos = self.arrow.transform.position.x
        
    def enableThrow(self):
        self.CanShoot = True

    def DrawArrow(self,window, camera):
        if self.arrow != None:
            self.arrow.Draw(window, camera)

    def Defence(self):
        self.shield = True

    def DesactivateDefence(self):
        self.shield = False
       

class Mob( Entity ):
    
    def __init__(
                    self,
                    
                    position: Vector2 = Vector2( 0, 0 ), #? Vector2( 500, 500 )
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    spritesheet_ref: SpriteSheetsRef = None,

                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),
                    isVisible: bool = True,
                    
                    velocity: Vector2 = Vector2( 0, 0 ), #? Vector2( 3, 3 )
                    
                    isOnLoop: bool = False,
                    pathPositions: LinkedList = None
                ):
        super().__init__( position, rotation, scale, spriteDimensions, None, spritesheet_ref, velocity )
        self.isOnLoop: bool = isOnLoop
        if ( self.isOnLoop ): self.pathDestination: LinkedList = pathPositions.first
        
        self.maximum_distance = 300
        self.maximum_throw_distance = 700
        self.CanThrow = True
        self.ThrowSpeed = 200
        self.Vecteur_directeur = pygame.Vector2(0,0)
        self.hammer = None
        self.shoot_timer = Timer(3, self.enableThrow )
        self.defence_timer = Timer(5, self.enableDefence )
        self.disable_shield_timer = Timer(1, self.disableShield )
        self.timer_between_attack = Timer(2,self.enableAttack )
        self.isFacingRight = False
        self.WalkSpeed = 100
        
        self.CanDefend = True
        self.shield = False
        self.CanAttack = True
        self.AttackRange = 50
        self.isAttacking = False
        self.isHit = False

    def movement( self, player: Player, dt, solidElements: list[GameObject]):
        if self.transform.position.distanceTo( player.transform.position ) < self.maximum_distance:
            if player.transform.position.x > self.transform.position.x:
                self.velocity.x = +1
                self.isFacingRight = True
            if player.transform.position.x < self.transform.position.x:
                self.velocity.x = -1
                self.isFacingRight = False

        collision: bool = False
        self.transform.position.x += self.WalkSpeed * dt * self.velocity.x
        for mapObject in solidElements: collision = collision or self.getCollision(mapObject)
        if (collision):
            self.transform.position.x -= self.WalkSpeed * dt * self.velocity.x
            self.velocity.x = 0

        self.velocity.y = 300

        collision: bool = False
        self.transform.position.y += self.velocity.y * dt
        print(self.velocity.y)
        for mapObject in solidElements: collision = collision or self.getCollision(mapObject)
        if (collision):
            self.transform.position.y -= self.velocity.y * dt
            self.velocity.y = 0

    def DamagePlayer(self, player: Player):
        if self.hammer != None:
            if self.hammer.getCollision(player) and player.shield == False:
                player.isHit = True
                self.hammer = None
                self.enableThrow()
                return
            elif  self.hammer.getCollision(player) and player.shield:
                self.hammer = None
                self.enableThrow()
                return



           
    def update(self, dt,  surface: pygame.Surface, camera: Vector2, mapElements: list[ GameObject ] ):
        self.shoot_timer.update(dt)
        self.defence_timer.update(dt)
        self.disable_shield_timer.update(dt)
        self.timer_between_attack.update(dt)


        self.transform.position += self.velocity
        if self.hammer != None:
            self.hammer.transform.position.x += self.Vecteur_directeur.x * self.ThrowSpeed * dt
            self.hammer.transform.position.y += self.Vecteur_directeur.y * self.ThrowSpeed * dt
        
        if self.velocity.x < 0:
            if self.shield:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.ENNEMY_SHIELD_LEFT
            elif self.isAttacking:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.ENNEMY_ATTACK_LEFT
            elif self.isHit:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.ENNEMY_GET_HIT_LEFT
            elif self.shield == False and self.isAttacking == False:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.ENNEMY_WALK_LEFT
        else:
            if self.shield:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.ENNEMY_SHIELD_RIGHT
            elif self.isAttacking:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.ENNEMY_ATTACK_RIGHT
            elif self.isHit:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.ENNEMY_GET_HIT_RIGHT
            elif self.shield == False and self.isAttacking == False:
                self.spriteRenderer.spriteSheetRef = SpriteSheetsRef.ENNEMY_WALK_RIGHT




        self.spriteRenderer.draw( surface, camera, self.transform, self.FinishAnim )


    def enableDefence(self):
        self.CanDefend = True

    def disableShield(self):
        self.shield = False
        self.defence_timer.start()
        

    def tryDefence(self, player: Player):
        if self.CanDefend == False:
            return
        
        if player.arrow != None and self.maximum_distance < self.transform.position.distanceTo( player.transform.position ) < self.maximum_throw_distance:
            self.shield = True
            self.CanDefend = False
            self.disable_shield_timer.start()


    
    def FinishAnim(self):
        self.isAttacking = False
        self.isHit = False


    def enableAttack(self):
        self.CanAttack = True

    def tryAttack(self, player: Player):
        if self.CanAttack == False:
            return
        
        if self.transform.position.distanceTo( player.transform.position ) < self.AttackRange:
            self.isAttacking = True
            self.CanAttack = False
            self.timer_between_attack.start()

            



    def enableThrow(self):
        self.CanThrow = True

    def tryThrow( self, player: Player, camera: Vector2):
        if self.CanThrow == False:
            return

        if self.maximum_distance < self.transform.position.distanceTo( player.transform.position ) < self.maximum_throw_distance:
            self.hammer = GameObject(position=Vector2(self.transform.position.x   ,self.transform.position.y  ))#, anchor=(0.5,0.5))
            self.Vecteur_directeur = Vector2(player.transform.position.x - self.transform.position.x, player.transform.position.y - self.transform.position.y )
            self.Vecteur_directeur.normalizeToSelf()
            self.CanThrow = False
            self.shoot_timer.start()




    def draw(self, window: pygame.Surface, player: Player, camera: Vector2):
        #pygame.draw.line(window, (255,255,255), (self.rect_transform.x + self.width // 2 ,self.rect_transform.y + self.height // 2), (self.Vecteur_directeur.x * self.maximum_throw_distance + player.rect_transform.width // 2  , self.Vecteur_directeur.y * self.maximum_throw_distance  + player.rect_transform.height // 2), 1)
        if self.hammer != None:
            Assets.GetSprite(SpritesRef.TOMAHAWK).draw(window,self.hammer.transform.position ,self.hammer.transform.scale)
        

        
