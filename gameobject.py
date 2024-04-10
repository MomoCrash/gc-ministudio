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
                    scale: Vector2 = Vector2( 1, 1 ),
                    anchor: Vector2 = Vector2( 0, 0 ),
                ):
        self.position: Vector2 = position
        self.rotation: Vector2 = rotation
        self.scale: Vector2 = scale
        self.anchor: Vector2 = anchor

    def getPosition(self, width, height):
        out: Vector2 = Vector2(0,0)
        out.x = self.position.x - width * self.anchor.x
        out.y =self.position.y - height * self.anchor.y 

        return out

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
        self.isVisible = isVisible
        
        if ( self.spriteRef == None and self.spriteSheetRef == None ):
            self.rect: pygame.Rect = pygame.Rect( transform.position.x, transform.position.y, transform.scale.x * self.dimensions.x, transform.scale.y * self.dimensions.y )
    
    def draw( self, surface: pygame.Surface, camera: Vector2, transform: Transform, callback = lambda: 0, dt: int=0 ) -> None:
        """Draws the sprite / sprite sheet / rectangle into the given surface (except if alpha color is 0)"""
        if ( not self.isVisible ): return
        if ( self.spriteSheetRef != None ): Assets.GetSpriteSheet( self.spriteSheetRef ).draw( dt, surface, transform.position - camera, self.dimensions * transform.scale, callback )
        elif ( self.spriteRef != None ): Assets.GetSprite( self.spriteRef ).draw( surface, transform.position - camera, self.dimensions * transform.scale )
        else:
            self.rect: pygame.Rect = pygame.Rect(transform.position.x - camera.x, transform.position.y - camera.y,
                                                 transform.scale.x * self.dimensions.x,
                                                 transform.scale.y * self.dimensions.y)
            pygame.draw.rect( surface, self.color, self.rect )

    def getWidth(self):
        if ( self.spriteSheetRef != None ): return Assets.GetSpriteSheet( self.spriteSheetRef ).textures[0].size[0]
        elif ( self.spriteRef != None ): return Assets.GetSprite( self.spriteRef ).size[0]
        else: return self.rect.right - self.rect.left 

    def getHeight(self):
        if ( self.spriteSheetRef != None ): return Assets.GetSpriteSheet( self.spriteSheetRef ).textures[1].size[1]
        elif ( self.spriteRef != None ): return Assets.GetSprite( self.spriteRef ).size[1]
        else: return self.rect.bottom - self.rect.top 



class GameObject:
    """Unity-like GameObject (2D) class that stores a Transform and a SpriteRenderer (TODO)"""
    def __init__(
                    self,         
                    
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),

                    spriteDimensions: Vector2 = Vector2( 1, 1 ),
                    spriteRef: SpritesRef = None,
                    spriteSheetRef: SpriteSheetsRef = None,
                    color: pygame.Color = pygame.Color( 255, 255, 255, 255 ),
                    isVisible: bool = True
                ):
        self.transform: Transform = Transform( position, rotation, scale )
        # print(spriteSheetRef)
        self.spriteRenderer: SpriteRenderer = SpriteRenderer( self.transform, spriteDimensions, spriteRef, spriteSheetRef, color, isVisible )
    
    def update( self, surface: pygame.Surface, camera: Vector2 ) -> None:
        self.spriteRenderer.draw( surface, camera, self.transform )
          
    def getCollision( self, other: GameObject | Vector2 ) -> bool:
        """Returns true if there is a collision between this GameObject and the one specified"""
        if ( isinstance( other, GameObject ) ):
            return \
            other.transform.position <= self.transform.position + ( self.spriteRenderer.dimensions * self.transform.scale ) and \
            other.transform.position + ( other.spriteRenderer.dimensions * other.transform.scale ) >= self.transform.position
        else:
            return self.transform.position <= other <= self.transform.position + ( self.spriteRenderer.dimensions * self.transform.scale )
    
    def isOnScreen( self, screenPosition: Vector2, screenSize: Vector2 ) -> bool:
        """Returns true if this GameObject is on the screen"""
        spriteDimensionsScaled: Vector2 = self.spriteRenderer.dimensions.multiplyToNew( self.transform.scale )
        return \
        self.transform.position.x + spriteDimensionsScaled.x >= screenPosition.x and \
        self.transform.position.x - spriteDimensionsScaled.x <= screenPosition.x + screenSize.x and \
        self.transform.position.y + spriteDimensionsScaled.y >= screenPosition.y and \
        self.transform.position.y - spriteDimensionsScaled.y <= screenPosition.y + screenSize.y
    
    def Move(self, direction, anchor_point = None):
        "fixer le point d'ancrage depuis lequel on veut faire bouger les points de notre GO"
        pass
    
    def GetWidth(self):
        return self.transform.scale.x * self.spriteRenderer.getWidth()
    
    def GetHeight(self):
        return self.transform.scale.y * self.spriteRenderer.getHeight()
    
    def Draw(self, window, camera):
        self.spriteRenderer.draw(window, camera, self.transform)