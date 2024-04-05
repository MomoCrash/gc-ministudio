from __future__ import annotations
from math import sqrt

class Vector2:
    def __init__( self, x: int, y: int ):
        self.x: int = x
        self.y: int = y
    
    def add( self, other: Vector2 ) -> None:
        self.x += other.x
        self.y += other.y
    
    def remove( self, other: Vector2 ) -> None:
        self.x -= other.x
        self.y -= other.y
    
    def norme( self ) -> int:
        return sqrt( self.x * self.x + self.y * self.y )
    
    def normalize( self ):
        norme: int = self.norme()
        self.x /= norme
        self.y /= norme
        
    def distance( self, other: Vector2 ):
        a = Vector2(other.x, other.y)
        a.remove(self)
        return a.norme()
        