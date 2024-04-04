import pygame



class Vector2:
    def __init__( self, x: int, y: int ):
        self.x = x
        self.y = y



class Transform:
    def __init__(
                    self,
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 )
                ):
        self.position = position
        self.rotation = rotation
        self.scale = scale



class GameObject:
    
    def __init__(
                    self,
                    position: Vector2 = Vector2( 0, 0 ),
                    rotation: Vector2 = Vector2( 0, 0 ),
                    scale: Vector2 = Vector2( 1, 1 ),
                    isTrigger: bool = False
                ):
        self.transform = Transform( position=position, rotation=rotation, scale=scale )
        self.rect = pygame.Rect( self.transform.position.x, self.transform.position.y, self.transform.scale.x, self.transform.scale.y )
        self.isTrigger = isTrigger
    
    def Draw( self, surface: pygame.Surface, color: pygame.Color ):
        pygame.draw.rect( surface, color, self.rect )
    
    def GetCollision( self, other: GameObject ) -> bool:
        
        return \
        other.transform.position.x < self.transform.position.x + self.transform.position.w and \
        other.transform.position.y < self.transform.position.y + self.transform.position.h and \
        other.transform.position.x + other.transform.position.w > self.transform.position.x and \
        other.transform.position.y + other.transform.position.h > self.transform.position.y
        
        # pygame.Rect.colliderect( self.rectTransform, otherRect )