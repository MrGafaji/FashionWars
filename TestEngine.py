import unittest
from GameEngine import Engine , sqState
from settings import settings

class EngineTest(unittest.TestCase):
    def testboardAxess(self):
        engine = Engine()
        # engine.setStartingState()
        engine.print2D()
        engine.print1D()
        # engine.findLegalMoves(0,1)


         



if __name__ == '__main__':
        unittest.main()
        