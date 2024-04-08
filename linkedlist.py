from __future__ import annotations



class Node:
    def __init__( self, value: any ):
        self.value = value
        self.previous = None
        self.next = None



class LinkedList:
    
    def __init__( self ):
        self.first = None
        self.count = 0
    
    def insertFirstTime( self, value: any ) -> bool:
        firstTime = self.first is None
        
        if ( firstTime ):
            self.first = Node( value )
            self.first.previous = self.first
            self.first.next = self.first
        
        return firstTime
    
    def insertAtBeginning( self, value: any ) -> None:
        self.count += 1
        if ( self.insertFirstTime( value ) ): return
        
        newNode = Node( value )
        newNode.previous = self.first.previous
        newNode.next = self.first
        self.first.previous.next = newNode
        self.first.previous = newNode
        self.first = newNode
    
    def insertAtEnd( self, value: any ) -> None:
        self.count += 1
        if ( self.insertFirstTime( value ) ): return
        
        newNode = Node( value )
        newNode.previous = self.first.previous
        newNode.next = self.first
        self.first.previous.next = newNode
        self.first.previous = newNode
    
    def removeAtBeginning( self ) -> None:
        if ( self.first is None ): return
        self.count -= 1
        self.first.previous.next = self.first.next
        self.first.next.previous = self.first.previous
        self.first = self.first.next
    
    def removeAtEnd( self ) -> None:
        if ( self.first is None ): return
        self.count -= 1
        self.first.previous.previous.next = self.first
        self.first.previous = self.first.previous.previous