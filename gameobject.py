from __future__ import annotations
import pygame
import json
from vector import Vector2
from texture import Assets, SpritesRef, SpriteSheetsRef



class Transform:
    """Unity-like Transform (2D) class that stores a position, a rotation and a scale"""
    def __init__(
                    self,
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 )
                ):
        self.position: Vector2 = position
        self.rotation: Vector2 = rotation
        self.scale: Vector2 = scale



class SpriteRenderer:
    """Unity-like SpriteRenderer (2D) class that stores a sprite or sprite sheet and it's dimensions as well as it's color"""
    def __init__(
                    self,
                    
                    transform: Transform,
                    
                    dimensions: Vector2 = Vector2( 1, 1 ),
                    spriteRef: SpritesRef = None,
                    spriteSheetRef: SpriteSheetsRef = None,
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),
                    isVisible: bool = True
                ):
        self.dimensions: Vector2 = dimensions
        self.spriteRef: SpritesRef = spriteRef
        self.spriteSheetRef: SpriteSheetsRef = spriteSheetRef
        self.color: pygame.Color = color
        self.isVisible: bool = isVisible
        
        if ( self.spriteRef == None and self.spriteSheetRef == None ):
            self.rect: pygame.Rect = pygame.Rect( transform.position.x, transform.position.y, transform.scale.x * self.dimensions.x, transform.scale.y * self.dimensions.y )
    
    def draw( self, surface: pygame.Surface, camera: Vector2, transform: Transform ) -> None:
        """Draws the sprite / sprite sheet / rectangle into the given surface (except if alpha color is 0)"""
        if ( not self.isVisible ): return
        if ( self.spriteSheetRef != None ): Assets.GetSpriteSheet( self.spriteSheetRef ).draw( pygame.time.get_ticks(), surface, transform.position.addToNew( camera ), self.dimensions.multiplyToNew( transform.scale ) )
        elif ( self.spriteRef != None ): Assets.GetSprite( self.spriteRef ).draw( surface, transform.position.addToNew( camera ), self.dimensions.multiplyToNew( transform.scale ) )
        else: 
          self.rect: pygame.Rect = pygame.Rect(transform.position.x - camera.x, transform.position.y - camera.y,
                                                 transform.scale.x * self.dimensions.x,
                                                 transform.scale.y * self.dimensions.y)
          pygame.draw.rect( surface, self.color, self.rect )



class GameObject:
    """Unity-like GameObject (2D) class that stores a Transform and a SpriteRenderer (TODO)"""
    def __init__(
                    self,
                    isActive: bool = True,
                    
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    spriteRef: SpritesRef = None,
                    spriteSheetRef: SpriteSheetsRef = None,
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),
                    isVisible: bool = True
                ):
        self.isActive: bool = isActive
        self.transform: Transform = Transform( position, rotation, scale )
        self.spriteRenderer: SpriteRenderer = SpriteRenderer( self.transform, spriteDimensions, spriteRef, spriteSheetRef, color, isVisible )
    
    def update( self, surface: pygame.Surface, camera: Vector2 ) -> None:
        if ( not self.isActive ): return
        self.spriteRenderer.draw( surface, camera, self.transform )
    
    def getCollision( self, other: GameObject ) -> bool:
        """Returns true if there is a collision between this GameObject and the one specified"""
        if ( not self.isActive ): return
        return \
        other.transform.position.x < self.transform.position.x + ( self.transform.scale.x * self.spriteRenderer.dimensions.x ) and \
        other.transform.position.y < self.transform.position.y + ( self.transform.scale.y  * self.spriteRenderer.dimensions.y ) and \
        other.transform.position.x + ( other.transform.scale.x * other.spriteRenderer.dimensions.x ) > self.transform.position.x and \
        other.transform.position.y + ( other.transform.scale.y * other.spriteRenderer.dimensions.y ) > self.transform.position.y
    
    def isOnScreen( self, screenPosition: Vector2, screenSize: Vector2 ) -> bool:
        """Returns true if this GameObject is on the screen"""
        spriteDimensionsScaled: Vector2 = self.spriteRenderer.dimensions.multiplyToNew( self.transform.scale )
        return \
        self.transform.position.x + spriteDimensionsScaled.x >= screenPosition.x and \
        self.transform.position.x - spriteDimensionsScaled.x <= screenPosition.x + screenSize.x and \
        self.transform.position.y + spriteDimensionsScaled.y >= screenPosition.y and \
        self.transform.position.y - spriteDimensionsScaled.y <= screenPosition.y + screenSize.y