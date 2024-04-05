class Node:
    def __init__( self, value: any, next: any = None ):
        self.value: any = value
        self.next: Node = next

class ChainedList:
    def __init__( self, first: Node, count: int = 0 ):
        self.first: Node = first
        self.count: int = count
    
    def append( self, value: any ) -> None:
        self.count += 1
        self.first = Node( value, self.first )
    
    def remove( self, index: int ):
        previousNode: Node = self.first
        for _ in range( index - 1 ):
            previousNode = previousNode.next
        node = previousNode.next
        nextNode = node.next
        previousNode.next = nextNode
        del node