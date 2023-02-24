class Stapel():
    class Node():
        def __init__(self, text):
            self.text = text

        def setNext(self, next):
            self.next = next

    def __init__(self):
        self._top = None

    def duw(self, item):
        newNode = self.Node(item)
        newNode.setNext(self._top)
        self._top = newNode
        

    def trek(self):
        if self.isLeeg():
            raise EmptyStackException()
        res = self._top.text
        self._top = self._top.next
        return res


    def top(self):
        if self.isLeeg():
            return None
        return self._top.text

    def isLeeg(self):
        return self._top is None

class EmptyStackException(Exception):
    pass