from __future__ import annotations
from math import sqrt



class Vector2:
    def __init__( self, x: int, y: int ):
        self.x: int = x
        self.y: int = y
    
    
    
    def copy( self ) -> Vector2:
        return Vector2( self.x, self.y )
    
    def scalarProduct( self, other: Vector2 ) -> int:
        return self.x * other.x + self.y * other.y
    
    def norm( self ) -> int:
        return sqrt( self.scalarProduct( self ) )
    
    def distanceTo( self, other: Vector2 ) -> int:
        return self.removeToNew( other ).norm()
        # return Vector2( self.x - other.x, self.y - other.y ).norm() #! Is this more efficient ?
    
    
    
    def addToSelf( self, other: Vector2 ) -> None:
        self.x += other.x
        self.y += other.y
    
    def removeToSelf( self, other: Vector2 ) -> None:
        self.x -= other.x
        self.y -= other.y
    
    def multiplyToSelf( self, other: Vector2 ) -> None:
        self.x *= other.x
        self.y *= other.y
    
    def divideToSelf( self, other: Vector2 ) -> None:
        self.x /= other.x
        self.y /= other.y
    
    def addToSelf( self, value: float ) -> None:
        self.x += value
        self.y += value
    
    def removeToSelf( self, value: float ) -> None:
        self.x -= value
        self.y -= value
    
    def multiplyToSelf( self, value: float ) -> None:
        self.x *= value
        self.y *= value
    
    def divideToSelf( self, value: float ) -> None:
        self.x /= value
        self.y /= value
    
    
    
    def addToNew( self, other: Vector2 ) -> Vector2:
        return Vector2( self.x + other.x, self.y + other.y )
    
    def removeToNew( self, other: Vector2 ) -> Vector2:
        return Vector2( self.x - other.x, self.y - other.y )
    
    def multiplyToNew( self, other: Vector2 ) -> Vector2:
        return Vector2( self.x * other.x, self.y * other.y )
    
    def divideToNew( self, other: Vector2 ) -> Vector2:
        return Vector2( self.x / other.x, self.y / other.y )
    
    def addToNew( self, value: float ) -> Vector2:
        return Vector2( self.x + value, self.y + value )
    
    def removeToNew( self, value: float ) -> Vector2:
        return Vector2( self.x - value, self.y - value )
    
    def multiplyToNew( self, value: float ) -> Vector2:
        return Vector2( self.x * value, self.y * value )
    
    def divideToNew( self, value: float ) -> Vector2:
        return Vector2( self.x / value, self.y / value )
    
    
    
    def normalizeToSelf( self ) -> None:
        self.divideToSelf( self.norm() )
    
    def normalizeToNew( self ) -> Vector2:
        return self.divideToNew( self.norm() )