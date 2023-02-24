

from bruikbaarheden import *
from GameMachine import Machine

class Computer():
    def __init__(self, team):
        self.team = team
        self.machine = Machine()

    def telOvernames(self, x,y):
        res = 0
        for m,n in self.machine.vindBuren(x,y):
            if self.machine.getCellState2D(m,n) == andereTeam(self.team):
                res += 1
        return res
        


    def speel(self, state):
        print("bob is playing!")
        self.machine.zetOpHetBord(state)
        # self.engine.print1D()
        if not self.machine.checkTeamHeeftLegaleZet(self.team):
            raise Exception("Ik heb geen zetten")

        ### determine computers squares
        mijnCellen = []
        for i in range(len(state)):
            if state[i] == self.team:
                mijnCellen.append(i)
        # print(f"{myCells = }")

        loop = self.vindBesteLoop(mijnCellen)
        spring = self.vindBesteSprong(mijnCellen)
        print(f"{loop = }  ,  {spring = }")

        if loop:
            fx,fy,tx,ty = loop
            return converteerCoordinaten1D(fx, fy), converteerCoordinaten1D(tx,ty)


        if spring:
            fx,fy,tx,ty = spring
            return converteerCoordinaten1D(fx, fy), converteerCoordinaten1D(tx,ty)
        
        raise Exception("Ik heb ECHT geen legale zetten!!")


        # print(f"{fx = }, {fy = }, {tx = }, {ty = }")


    def vindBesteLoop(self, myCells):
        fx = None
        numOvernames = 0
        for ix in myCells:
            x, y = converteerCoordinaten2D(ix)
            ### finding Best Move
            zetten = self.machine.vindLegaleLoopjes(x,y)

            # print(f"{moves = } , {x = } , {y = }")

            for a,b in zetten:
                if fx == None or self.telOvernames(a,b) > numOvernames:
                    fx, fy = x,y
                    tx, ty = a,b
                    numOvernames = self.telOvernames(a,b)

        if fx == None:
            return
        return fx,fy,tx,ty
        
    def vindBesteSprong(self, myCells):
        numOvernames = 0
        fx = None
        for ix in myCells:
            x, y = converteerCoordinaten2D(ix)
            ### finding Best Move
            zetten = self.machine.vindLegaleSprongen(x,y)

            # print(f"{moves = } , {x = } , {y = }")

            for a,b in zetten:
                if fx == None or self.telOvernames(a,b) > numOvernames:
                    fx, fy = x,y
                    tx, ty = a,b
                    numOvernames = self.telOvernames(a,b)
        if fx == None:
            return
        return fx,fy,tx,ty
            
        
