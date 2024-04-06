from __future__ import annotations
from math import sqrt

class Vector2:
    def __init__( self, x: float, y: float ):
        self.x: float = x
        self.y: float = y
    
    
    
    def copy( self ) -> Vector2:
        return Vector2( self.x, self.y )
    
    def scalarProduct( self, other: Vector2 ) -> float:
        return self.x * other.x + self.y * other.y
    
    def norm( self ) -> float:
        return sqrt( self.scalarProduct( self ) )
    
    def distanceTo( self, other: Vector2 ) -> float:
        return self.removeToNew( other ).norm()
        # return Vector2( self.x - other.x, self.y - other.y ).norm() #! Is this more efficient ?
    
    
    
    def addToSelf( self, other: Vector2 | float ) -> None:
        if isinstance( other, Vector2 ):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
    
    def removeToSelf( self, other: Vector2 | float ) -> None:
        if isinstance( other, Vector2 ):
            self.x -= other.x
            self.y -= other.y
        else:
            self.x -= other
            self.y -= other
    
    def multiplyToSelf( self, other: Vector2 | float ) -> None:
        if isinstance( other, Vector2 ):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
    
    def divideToSelf( self, other: Vector2 | float ) -> None:
        if isinstance( other, Vector2 ):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
    
    
    
    def addToNew( self, other: Vector2 | float ) -> Vector2:
        newVector = self.copy()
        newVector.addToSelf( other )
        return newVector
    
    def removeToNew( self, other: Vector2 | float ) -> Vector2:
        newVector = self.copy()
        newVector.removeToSelf( other )
        return newVector
    
    def multiplyToNew( self, other: Vector2 | float ) -> Vector2:
        newVector = self.copy()
        newVector.multiplyToSelf( other )
        return newVector
    
    def divideToNew( self, other: Vector2 | float ) -> Vector2:
        newVector = self.copy()
        newVector.divideToSelf( other )
        return newVector
    
    
    
    def normalizeToSelf( self ) -> None:
        self.divideToSelf( self.norm() )
    
    def normalizeToNew( self ) -> Vector2:
        return self.divideToNew( self.norm() )
