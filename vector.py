from __future__ import annotations
from math import sqrt



class Vector2:
    def __init__( self, x: int, y: int ):
        self.x: int = x
        self.y: int = y
    
    def Copy( self ) -> Vector2:
        return Vector2( self.x, self.y )
    
    def ScalarProduct( self, other: Vector2 ) -> int:
        return self.x * other.x + self.y * other.y
    
    def Norm( self ) -> int:
        return sqrt( self.ScalarProduct( self ) )
    
    def DistanceTo( self, other: Vector2 ) -> int:
        return Vector2( self.x - other.x, self.y - other.y ).Norm()
    
    def Add( self, other: Vector2 ) -> None:
        self.x += other.x
        self.y += other.y
    
    def Remove( self, other: Vector2 ) -> None:
        self.x -= other.x
        self.y -= other.y
    
    def Normalize( self ) -> None:
        norm: int = self.Norm()
        self.x /= norm
        self.y /= norm



class Vector3:
    def __init__( self, x: int, y: int, z: int ):
        self.x: int = x
        self.y: int = y
        self.z: int = z
    
    def Copy( self ) -> Vector3:
        return Vector3( self.x, self.y, self.z )
    
    def ScalarProduct( self, other: Vector3 ) -> int:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def Norm( self ) -> int:
        return sqrt( self.ScalarProduct( self ) )
    
    def DistanceTo( self, other: Vector3 ) -> int:
        return Vector3( self.x - other.x, self.y - other.y, self.z - other.z ).Norm()
    
    def Add( self, other: Vector3 ) -> None:
        self.x += other.x
        self.y += other.y
        self.z += other.z
    
    def Remove( self, other: Vector3 ) -> None:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
    
    def Normalize( self ) -> None:
        norm: int = self.Norm()
        self.x /= norm
        self.y /= norm
        self.z /= norm