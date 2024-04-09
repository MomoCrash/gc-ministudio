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
    

    def __add__( self, other: Vector2 | float ) -> Vector2: # Vector2 + ( Vector2 | float )
        newVector = self.copy()
        if isinstance( other, Vector2 ):
            newVector.x += other.x
            newVector.y += other.y
        else:
            newVector.x += other
            newVector.y += other
        return newVector
        # return Vector2( self.x + other.x, self.y + other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x + other, self.y + other )
    
    def normalizeToSelf( self ) -> None:
        self.divideToSelf( self.norm() )
    
    def normalizeToNew( self ) -> Vector2:
        return self.divideToNew( self.norm() )

    def __sub__(self, other: Vector2 | float) -> Vector2:  # Vector2 - ( Vector2 | float )
        newVector = self.copy()
        if isinstance(other, Vector2):
            newVector.x -= other.x
            newVector.y -= other.y
        else:
            newVector.x -= other
            newVector.y -= other
        return newVector
        # return Vector2( self.x - other.x, self.y - other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x - other, self.y - other )

    def __mul__(self, other: Vector2 | float) -> Vector2:  # Vector2 * ( Vector2 | float )
        newVector = self.copy()
        if isinstance(other, Vector2):
            newVector.x *= other.x
            newVector.y *= other.y
        else:
            newVector.x *= other
            newVector.y *= other
        return newVector
        # return Vector2( self.x * other.x, self.y * other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x * other, self.y * other )

    def __truediv__(self, other: Vector2 | float) -> Vector2:  # Vector2 / ( Vector2 | float )
        newVector = self.copy()
        if isinstance(other, Vector2):
            newVector.x /= other.x
            newVector.y /= other.y
        else:
            newVector.x /= other
            newVector.y /= other
        return newVector
        # return Vector2( self.x / other.x, self.y / other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x / other, self.y / other )

    def __floordiv__(self, other: Vector2 | float) -> Vector2:  # Vector2 // ( Vector2 | float )
        newVector = self.copy()
        if isinstance(other, Vector2):
            newVector.x //= other.x
            newVector.y //= other.y
        else:
            newVector.x //= other
            newVector.y //= other
        return newVector
        # return Vector2( self.x // other.x, self.y // other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x // other, self.y // other )

    def __mod__(self, other: Vector2 | float) -> Vector2:  # Vector2 % ( Vector2 | float )
        newVector = self.copy()
        if isinstance(other, Vector2):
            newVector.x %= other.x
            newVector.y %= other.y
        else:
            newVector.x %= other
            newVector.y %= other
        return newVector
        # return Vector2( self.x % other.x, self.y % other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x % other, self.y % other )

    def __pow__(self, other: Vector2 | float) -> Vector2:  # Vector2 ** ( Vector2 | float )
        newVector = self.copy()
        if isinstance(other, Vector2):
            newVector.x **= other.x
            newVector.y **= other.y
        else:
            newVector.x **= other
            newVector.y **= other
        return newVector
        # return Vector2( self.x ** other.x, self.y ** other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x ** other, self.y ** other )

    def __lshift__(self, other: Vector2 | float) -> Vector2:  # Vector2 << ( Vector2 | float )
        newVector = self.copy()
        if isinstance(other, Vector2):
            newVector.x <<= other.x
            newVector.y <<= other.y
        else:
            newVector.x <<= other
            newVector.y <<= other
        return newVector
        # return Vector2( self.x << other.x, self.y << other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x << other, self.y << other )

    def __rshift__(self, other: Vector2 | float) -> Vector2:  # Vector2 >> ( Vector2 | float )
        newVector = self.copy()
        if isinstance(other, Vector2):
            newVector.x >>= other.x
            newVector.y >>= other.y
        else:
            newVector.x >>= other
            newVector.y >>= other
        return newVector
        # return Vector2( self.x >> other.x, self.y >> other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x >> other, self.y >> other )

    def __divmod__(self, other: Vector2 | float) -> tuple[Vector2]:  # ?
        return (self // other, self % other)

    def __and__(self, other: Vector2) -> bool:  # Vector2 & Vector2
        return (self.x or self.y) and (other.x or other.y)

    def __or__(self, other: Vector2) -> bool:  # Vector2 | Vector2
        return (self.x or self.y) or (other.x or other.y)

    def __xor__(self, other: Vector2) -> bool:  # Vector2 ^ Vector2
        return (self | other) and not (self & other)

    def __lt__(self, other: Vector2) -> bool:  # Vector2 < Vector2
        return (self.x < other.x) and (self < other.x)

    def __rt__(self, other: Vector2) -> bool:  # Vector2 > Vector2
        return (self.x > other.x) and (self > other.x)