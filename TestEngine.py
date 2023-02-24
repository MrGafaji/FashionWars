import unittest
from GameMachine import Machine , sqState
from instellingen import instellingen

class EngineTest(unittest.TestCase):
    def testboardAxess(self):
        engine = Machine()
        # engine.setStartingState()
        engine.print2D()
        engine.print1D()
        # engine.findLegalMoves(0,1)


         



if __name__ == '__main__':
        unittest.main()
        