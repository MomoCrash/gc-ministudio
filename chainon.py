from __future__ import annotations

class Node:
    def __init__( self, value: any, previous: Node = None, next: Node = None ):
        self.value: any = value
        self.previous: Node = previous
        self.next: Node = next

class ChainedList:
    def __init__( self, elements: list[ any ] ):
        self.first: Node = Node( elements[ 0 ] )
        node = self.first
        self.count: int = 1
        for e in elements:
            node.next = Node( e, node )
            node = node.next
            self.count += 1
        node.next = self.first
        self.first.previous = node
    
    def append( self, value: any ) -> None:
        newNode = Node( value, self.first.previous, self.first )
        self.first.previous.next = newNode
        self.first.previous = newNode
        self.count += 1
    
    def remove( self ) -> None:
        if self.count <= 0: return
        self.first.previous.previous.next = self.first
        self.first.previous = self.first.previous.previous
        self.count -= 1



# a = ChainedList( [ 0, 1, 2 ] )
# print( a.first.previous.value, a.first.previous.next.value, a.first.value, a.first.next.previous.value, a.first.next.value )
# a.first.value = 3
# print( a.first.previous.value, a.first.previous.next.value, a.first.value, a.first.next.previous.value, a.first.next.value )