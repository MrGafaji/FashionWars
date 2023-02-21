class Stack():
    class Node():
        def __init__(self, text):
            self.text = text

        def setNext(self, next):
            self.next = next

    def __init__(self):
        self._top = None

    def push(self, item):
        newNode = self.Node(item)
        newNode.setNext(self._top)
        self._top = newNode
        

    def pop(self):
        if self.isEmpty():
            raise EmptyStackException()
        res = self._top.text
        self._top = self._top.next
        return res


    def top(self):
        if self.isEmpty():
            return None
        return self._top.text

    def isEmpty(self):
        return self._top is None

class EmptyStackException(Exception):
    """raised when trying to pop from empty stack"""
    pass