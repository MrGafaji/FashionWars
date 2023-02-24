

from settings import settings
from utils import *
from GameEngine import Engine

class Computer():
    def __init__(self, team):
        self.team = team
        self.engine = Engine()

    def countOvertakes(self, x,y):
        res = 0
        for m,n in self.engine.findNeighbours(x,y):
            if self.engine.getCellState2D(m,n) == otherTeam(self.team):
                res += 1
        return res
        


    def play(self, state):
        print("bob is playing!")
        self.engine.setBoardState(state)
        # self.engine.print1D()
        if not self.engine.checkTeamHasLegalMove(self.team):
            raise Exception("I have no legal moves")

        ### determine computers squares
        myCells = []
        for i in range(len(state)):
            if state[i] == self.team:
                myCells.append(i)
        # print(f"{myCells = }")

        walk = self.findBestWalk(myCells)
        jump = self.findBestJump(myCells)
        print(f"{walk = }  ,  {jump = }")

        if walk:
            fx,fy,tx,ty = walk
            return convertCoordinates1D(fx, fy), convertCoordinates1D(tx,ty)


        if jump:
            fx,fy,tx,ty = jump
            return convertCoordinates1D(fx, fy), convertCoordinates1D(tx,ty)
        
        raise Exception("I have no legal moves Bitch")


        # print(f"{fx = }, {fy = }, {tx = }, {ty = }")


    def findBestWalk(self, myCells):
        fx = None
        numOvertakes = 0
        for ix in myCells:
            x, y = convertCoordinates2D(ix)
            ### finding Best Move
            moves = self.engine.findLegalWalks(x,y)

            # print(f"{moves = } , {x = } , {y = }")

            for a,b in moves:
                if fx == None or self.countOvertakes(a,b) > numOvertakes:
                    fx, fy = x,y
                    tx, ty = a,b
                    numOvertakes = self.countOvertakes(a,b)

        if fx == None:
            return
        return fx,fy,tx,ty
        
    def findBestJump(self, myCells):
        numOvertakes = 0
        fx = None
        for ix in myCells:
            x, y = convertCoordinates2D(ix)
            ### finding Best Move
            moves = self.engine.findLegalJumps(x,y)

            # print(f"{moves = } , {x = } , {y = }")

            for a,b in moves:
                if fx == None or self.countOvertakes(a,b) > numOvertakes:
                    fx, fy = x,y
                    tx, ty = a,b
                    numOvertakes = self.countOvertakes(a,b)
        if fx == None:
            return
        return fx,fy,tx,ty
            
        
