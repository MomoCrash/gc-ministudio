from __future__ import annotations

class Vector2:
    def __init__( self, x: float, y: float ):
        self.x: float = x
        self.y: float = y
    
    def __repr__( self ):
        return f"({self.x}, {self.y})"
    
    def copy( self ) -> Vector2:
        return Vector2( self.x, self.y )
    
    
    
    def scalarProduct( self, other: Vector2 ) -> float:
        return self.x * other.x + self.y * other.y
    
    def norm( self ) -> float:
        return self.scalarProduct( self )**0.5
    
    def normalizeToSelf( self ) -> None:
        n = self.norm()
        self.x /= n
        self.y /= n
    
    def normalizeToNew( self ) -> Vector2:
        return self / self.norm()
    
    def distanceTo( self, other: Vector2 ) -> float:
        return Vector2(self.x - other.x, self.y - other.y).norm()
    
    def abs( self ) -> None: # Vector2.abs()
        self.x *= 1 if self.x >= 0 else -1
        self.y *= 1 if self.y >= 0 else -1
    
    def __abs__( self ) -> Vector2: # abs( Vector2 )
        return Vector2( self.x if self.x >= 0 else -self.x , self.y if self.y >= 0 else -self.y )

    
    
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
    
    def __sub__( self, other: Vector2 | float ) -> Vector2: # Vector2 - ( Vector2 | float )
        newVector = self.copy()
        if isinstance( other, Vector2 ):
            newVector.x -= other.x
            newVector.y -= other.y
        else:
            newVector.x -= other
            newVector.y -= other
        return newVector
        # return Vector2( self.x - other.x, self.y - other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x - other, self.y - other )
    
    def __mul__( self, other: Vector2 | float ) -> Vector2: # Vector2 * ( Vector2 | float )
        newVector = self.copy()
        if isinstance( other, Vector2 ):
            newVector.x *= other.x
            newVector.y *= other.y
        else:
            newVector.x *= other
            newVector.y *= other
        return newVector
        # return Vector2( self.x * other.x, self.y * other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x * other, self.y * other )
    
    def __truediv__( self, other: Vector2 | float ) -> Vector2: # Vector2 / ( Vector2 | float )
        newVector = self.copy()
        if isinstance( other, Vector2 ):
            newVector.x /= other.x
            newVector.y /= other.y
        else:
            newVector.x /= other
            newVector.y /= other
        return newVector
        # return Vector2( self.x / other.x, self.y / other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x / other, self.y / other )
    
    def __floordiv__( self, other: Vector2 | float ) -> Vector2: # Vector2 // ( Vector2 | float )
        newVector = self.copy()
        if isinstance( other, Vector2 ):
            newVector.x //= other.x
            newVector.y //= other.y
        else:
            newVector.x //= other
            newVector.y //= other
        return newVector
        # return Vector2( self.x // other.x, self.y // other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x // other, self.y // other )
    
    def __mod__( self, other: Vector2 | float ) -> Vector2: # Vector2 % ( Vector2 | float )
        newVector = self.copy()
        if isinstance( other, Vector2 ):
            newVector.x %= other.x
            newVector.y %= other.y
        else:
            newVector.x %= other
            newVector.y %= other
        return newVector
        # return Vector2( self.x % other.x, self.y % other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x % other, self.y % other )
    
    def __pow__( self, other: Vector2 | float ) -> Vector2: # Vector2 ** ( Vector2 | float )
        newVector = self.copy()
        if isinstance( other, Vector2 ):
            newVector.x **= other.x
            newVector.y **= other.y
        else:
            newVector.x **= other
            newVector.y **= other
        return newVector
        # return Vector2( self.x ** other.x, self.y ** other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x ** other, self.y ** other )
    
    def __lshift__( self, other: Vector2 | float ) -> Vector2: # Vector2 << ( Vector2 | float )
        newVector = self.copy()
        if isinstance( other, Vector2 ):
            newVector.x <<= other.x
            newVector.y <<= other.y
        else:
            newVector.x <<= other
            newVector.y <<= other
        return newVector
        # return Vector2( self.x << other.x, self.y << other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x << other, self.y << other )
    
    def __rshift__( self, other: Vector2 | float ) -> Vector2: # Vector2 >> ( Vector2 | float )
        newVector = self.copy()
        if isinstance( other, Vector2 ):
            newVector.x >>= other.x
            newVector.y >>= other.y
        else:
            newVector.x >>= other
            newVector.y >>= other
        return newVector
        # return Vector2( self.x >> other.x, self.y >> other.y ) if ( isinstance( other, Vector2 ) ) else Vector2( self.x >> other, self.y >> other )
    
    def __divmod__( self, other: Vector2 | float ) -> tuple[ Vector2 ]: # ?
        return ( self // other, self % other )
    
    
    
    def __bool__( self ) -> bool: # Vector2
        return bool( self.x ) or bool( self.y )
    
    def __and__( self, other: Vector2 ) -> bool: # Vector2 & Vector2
        return ( bool( self.x ) or bool( self.y ) ) and ( bool( other.x ) or bool( other.y ) )
    
    def __or__( self, other: Vector2 ) -> bool: # Vector2 | Vector2
        return ( bool( self.x ) or bool( self.y ) ) or ( bool( other.x ) or bool( other.y ) )
    
    def __xor__( self, other: Vector2 ) -> bool: # Vector2 ^ Vector2
        return ( self | other ) and not ( self & other )
    
    def __lt__( self, other: Vector2 ) -> bool: # Vector2 < Vector2
        return ( self.x < other.x ) and ( self.y < other.y )
    
    def __rt__( self, other: Vector2 ) -> bool: # Vector2 > Vector2
        return ( self.x > other.x ) and ( self.y > other.y )
    
    def __le__( self, other: Vector2 ) -> bool: # Vector2 < Vector2
        return ( self.x <= other.x ) and ( self.y <= other.y )
    
    def __re__( self, other: Vector2 ) -> bool: # Vector2 > Vector2
        return ( self.x >= other.x ) and ( self.y >= other.y )