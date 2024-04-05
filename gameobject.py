from __future__ import annotations
import pygame
from texture import *
from math import sqrt



class Vector2:
    def __init__( self, x: int, y: int ):
        self.x: int = x
        self.y: int = y
    
    def add( self, other: Vector2 ) -> None:
        self.x += other.x
        self.y += other.y
    
    def remove( self, other: Vector2 ) -> None:
        self.x -= other.x
        self.y -= other.y
    
    def norme( self ) -> int:
        return sqrt( self.x * self.x + self.y * self.y )
    
    def normalize( self ):
        norme: int = self.norme()
        self.x /= norme
        self.y /= norme



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
                    isVisible: bool = True
                ):
        self.transform: Transform = Transform( position, rotation, scale )
        self.sprite: Sprite = sprite
        self.spriteSheet: SpriteSheet = spriteSheet
        if ( self.sprite == None and self.spriteSheet == None ):
            self.rect: pygame.Rect = pygame.Rect( self.transform.position.x, self.transform.position.y, self.transform.scale.x, self.transform.scale.y )
        self.isVisible: bool = isVisible
    
    def draw( self, surface: pygame.Surface, color: pygame.Color = pygame.Color( 255, 255, 255 ) ) -> None:
        if ( not self.isVisible ): return
        if ( self.spriteSheet != None ): self.spriteSheet.draw( pygame.time.get_ticks(), surface, self.transform.position )
        elif ( self.sprite != None ): self.sprite.draw( surface, self.transform.position )
        else: pygame.draw.rect( surface, color, self.rect )
    
    def GetCollision( self, otherTransform: Transform ) -> bool:
        return \
        otherTransform.position.x < self.transform.position.x + self.transform.scale.x and \
        otherTransform.position.y < self.transform.position.y + self.transform.scale.y and \
        otherTransform.position.x + otherTransform.scale.x > self.transform.position.x and \
        otherTransform.position.y + otherTransform.scale.y > self.transform.position.y