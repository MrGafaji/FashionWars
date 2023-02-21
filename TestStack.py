import unittest
from Stack import Stack, EmptyStackException

class StackTest(unittest.TestCase):
    def testTop(self):
        teststr = "item"
        stack = Stack()
        self.assertIsNone(stack.top(),"Stack initially not empty")
        stack.push(teststr)
        self.assertEqual(teststr, stack.top())

    def testIsEmpty(self):
        teststr = "item"
        stack = Stack()
        self.assertTrue(stack.isEmpty())
        stack.push(teststr)
        self.assertFalse(stack.isEmpty())

    def testPush(self):
        teststr1 = 5
        teststr2 = {}
        teststr3 = "item3"
        stack = Stack()
        stack.push(teststr1)
        self.assertEqual(teststr1, stack.top())
        stack.push(teststr2)
        self.assertEqual(teststr2, stack.top())
        stack.push(teststr3)
        self.assertEqual(teststr3, stack.top())


    def testPop(self):
        teststr1 = "item1"
        teststr2 = "item2"
        teststr3 = "item3"
        stack = Stack()
        stack.push(teststr1)
        stack.push(teststr2)
        self.assertEqual(teststr2, stack.pop())
        stack.push(teststr3)
        self.assertEqual(teststr3, stack.pop())
        self.assertEqual(teststr1, stack.pop())


    def testEmptyStackException(self):
        stack = Stack()
        try:
            stack.pop()
        except EmptyStackException as e:
            pass            
            
            


if __name__ == '__main__':
        unittest.main()
