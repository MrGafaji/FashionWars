import unittest
from stapel import Stapel, EmptyStackException

class StackTest(unittest.TestCase):
    def testTop(self):
        teststr = "item"
        stack = Stapel()
        self.assertIsNone(stack.top(),"Stack initially not empty")
        stack.duw(teststr)
        self.assertEqual(teststr, stack.top())

    def testIsEmpty(self):
        teststr = "item"
        stack = Stapel()
        self.assertTrue(stack.isLeeg())
        stack.duw(teststr)
        self.assertFalse(stack.isLeeg())

    def testPush(self):
        teststr1 = 5
        teststr2 = {}
        teststr3 = "item3"
        stack = Stapel()
        stack.duw(teststr1)
        self.assertEqual(teststr1, stack.top())
        stack.duw(teststr2)
        self.assertEqual(teststr2, stack.top())
        stack.duw(teststr3)
        self.assertEqual(teststr3, stack.top())


    def testPop(self):
        teststr1 = "item1"
        teststr2 = "item2"
        teststr3 = "item3"
        stack = Stapel()
        stack.duw(teststr1)
        stack.duw(teststr2)
        self.assertEqual(teststr2, stack.trek())
        stack.duw(teststr3)
        self.assertEqual(teststr3, stack.trek())
        self.assertEqual(teststr1, stack.trek())


    def testEmptyStackException(self):
        stack = Stapel()
        try:
            stack.trek()
        except EmptyStackException as e:
            pass            
            
            


if __name__ == '__main__':
        unittest.main()
