from __future__ import annotations
import pygame
from vector import Vector2
from texture import Sprite, SpriteSheet


class Transform:
    def __init__(
                    self,
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 )
                ):
        self.position: Vector2 = position
        self.rotation: Vector2 = rotation
        self.scale: Vector2 = scale



class GameObject:
    
    def __init__(
                    self,         
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    sprite: Sprite = None,
                    spriteSheet: SpriteSheet = None,
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    isVisible: bool = True
                ):
        self.transform: Transform = Transform( position, rotation, scale )
        self.sprite: Sprite = sprite
        self.spriteSheet: SpriteSheet = spriteSheet
        self.spriteDimensions: Vector2 = spriteDimensions
        self.isVisible: bool = isVisible
        
        if ( self.sprite == None and self.spriteSheet == None ):
            self.rect: pygame.Rect = pygame.Rect( self.transform.position.x, self.transform.position.y, self.transform.scale.x * self.spriteDimensions.x, self.transform.scale.y * self.spriteDimensions.y ) #! Don't forget to replace this line with "isVisible = False"
    
    def update( self, surface: pygame.Surface ) -> None:
        self.draw( surface )
    
    def draw( self, surface: pygame.Surface, color: pygame.Color = pygame.Color( 255, 255, 255 ) ) -> None: #! Don't forget to remove the "color" because it's only for testing
        if ( not self.isVisible ): return
        if ( self.spriteSheet != None ): self.spriteSheet.draw( pygame.time.get_ticks(), surface, self.transform.position, self.spriteDimensions.multiplyToNew( self.transform.scale ) )
        elif ( self.sprite != None ): self.sprite.draw( surface, self.transform.position, self.spriteDimensions.multiplyToNew( self.transform.scale ) )
        else: pygame.draw.rect( surface, color, self.rect ) #! Don't forget to remove this line because it's only for testing
    
    def getCollision( self, other: GameObject ) -> bool:
        return \
        other.transform.position.x < self.transform.position.x + ( self.transform.scale.x * self.spriteDimensions.x ) and \
        other.transform.position.y < self.transform.position.y + ( self.transform.scale.y  * self.spriteDimensions.y ) and \
        other.transform.position.x + ( other.transform.scale.x * other.spriteDimensions.x ) > self.transform.position.x and \
        other.transform.position.y + ( other.transform.scale.y * other.spriteDimensions.y ) > self.transform.position.y
