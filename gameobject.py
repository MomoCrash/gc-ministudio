from __future__ import annotations
import pygame
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
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 )
                ):
        self.dimensions: Vector2 = dimensions
        self.spriteRef: SpritesRef = spriteRef
        self.spriteSheetRef: SpriteSheetsRef = spriteSheetRef
        self.color: pygame.Color = color
        
        if ( self.spriteRef == None and self.spriteSheetRef == None ):
            self.rect: pygame.Rect = pygame.Rect( transform.position.x, transform.position.y, transform.scale.x * self.dimensions.x, transform.scale.y * self.dimensions.y )
    
    def draw( self, surface: pygame.Surface, transform: Transform ) -> None:
        """Draws the sprite / sprite sheet / rectangle into the given surface (except if alpha color is 0)"""
        if ( self.color.a == 0 ): return
        if ( self.spriteSheetRef != None ): Assets.GetSpriteSheet( self.spriteSheetRef ).draw( pygame.time.get_ticks(), surface, transform.position, self.dimensions.multiplyToNew( transform.scale ) )
        elif ( self.spriteRef != None ): Assets.GetSprite( self.spriteRef ).draw( surface, transform.position, self.dimensions.multiplyToNew( transform.scale ) )
        else: pygame.draw.rect( surface, self.color, self.rect )



class GameObject:
    """Unity-like GameObject (2D) class that stores a Transform and a SpriteRenderer (TODO)"""
    def __init__(
                    self,         
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    
                    spriteRef: SpritesRef = None,
                    spriteSheetRef: SpriteSheetsRef = None,
                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    isVisible: bool = True,
                    color: pygame.Color = pygame.Color( 255, 255, 255 )
                ):
        self.transform: Transform = Transform( position, rotation, scale )
        self.spriteRef: SpritesRef = spriteRef
        self.spriteSheetRef: SpriteSheetsRef = spriteSheetRef
        self.spriteDimensions: Vector2 = spriteDimensions
        self.isVisible: bool = isVisible
        
        if ( self.spriteRef == None and self.spriteSheetRef == None ):
            self.rect: pygame.Rect = pygame.Rect( self.transform.position.x, self.transform.position.y, self.transform.scale.x * self.spriteDimensions.x, self.transform.scale.y * self.spriteDimensions.y )
            self.color: pygame.Color = color
    
    def update( self, surface: pygame.Surface ) -> None:
        self.draw( surface )
    
    def draw( self, surface: pygame.Surface ) -> None:
        """Draws the sprite / sprite sheet / rectangle into the given surface (except if not visible)"""
        if ( not self.isVisible ): return
        if ( self.spriteSheetRef != None ): Assets.GetSpriteSheet( self.spriteSheetRef ).draw( pygame.time.get_ticks(), surface, self.transform.position, self.spriteDimensions.multiplyToNew( self.transform.scale ) )
        elif ( self.spriteRef != None ): Assets.GetSprite( self.spriteRef ).draw( surface, self.transform.position, self.spriteDimensions.multiplyToNew( self.transform.scale ) )
        else: pygame.draw.rect( surface, self.color, self.rect )
    
    def getCollision( self, other: GameObject ) -> bool:
        """Returns true if there is a collision between this GameObject and the one specified"""
        return \
        other.transform.position.x < self.transform.position.x + ( self.transform.scale.x * self.spriteDimensions.x ) and \
        other.transform.position.y < self.transform.position.y + ( self.transform.scale.y  * self.spriteDimensions.y ) and \
        other.transform.position.x + ( other.transform.scale.x * other.spriteDimensions.x ) > self.transform.position.x and \
        other.transform.position.y + ( other.transform.scale.y * other.spriteDimensions.y ) > self.transform.position.y
    
    def isOnScreen( self, screenPosition: Vector2, screenSize: Vector2 ) -> bool:
        """Returns true if this GameObject is on the screen"""
        spriteDimensionsScaled: Vector2 = self.spriteDimensions.multiplyToNew( self.transform.scale )
        return \
        self.transform.position.x + spriteDimensionsScaled.x >= screenPosition.x and \
        self.transform.position.x - spriteDimensionsScaled.x <= screenPosition.x + screenSize.x and \
        self.transform.position.y + spriteDimensionsScaled.y >= screenPosition.y and \
        self.transform.position.y - spriteDimensionsScaled.y <= screenPosition.y + screenSize.y