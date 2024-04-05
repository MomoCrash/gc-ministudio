from __future__ import annotations



class Node:
    def __init__( self, value: any, next: Node = None ):
        self.value = value
        self.next = next



class LinkedList:
    
    def __init__( self ):
        self.first = None
    
    def insertFirst( self, value: any ) -> None:
        newNode = Node( value )
        
        if ( self.first is None ):
            self.first = newNode
            return
    
        newNode.next = self.first
        self.first = newNode
    
    def removeFirst( self ) -> None:
        if ( self.first is None ): return
        self.first = self.first.next