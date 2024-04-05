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
        return Vector2( self.x - other.x, self.y - other.y ).norm()
    
    def add( self, other: Vector2 ) -> None:
        self.x += other.x
        self.y += other.y
    
    def remove( self, other: Vector2 ) -> None:
        self.x -= other.x
        self.y -= other.y
    
    def normalize( self ) -> None:
        norm: int = self.norm()
        self.x /= norm
        self.y /= norm



class Vector3:
    def __init__( self, x: int, y: int, z: int ):
        self.x: int = x
        self.y: int = y
        self.z: int = z
    
    def copy( self ) -> Vector3:
        return Vector3( self.x, self.y, self.z )
    
    def scalarProduct( self, other: Vector3 ) -> int:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def norm( self ) -> int:
        return sqrt( self.scalarProduct( self ) )
    
    def distanceTo( self, other: Vector3 ) -> int:
        return Vector3( self.x - other.x, self.y - other.y, self.z - other.z ).norm()
    
    def add( self, other: Vector3 ) -> None:
        self.x += other.x
        self.y += other.y
        self.z += other.z
    
    def remove( self, other: Vector3 ) -> None:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
    
    def normalize( self ) -> None:
        norm: int = self.norm()
        self.x /= norm
        self.y /= norm
        self.z /= norm