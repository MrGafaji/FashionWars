from instellingen import instellingen
from bruikbaarheden import *
from stapel import Stapel



class Machine():
    class Cell():
        def __init__(self):
            self.state = sqState.empty
        def setLeeg(self):
            self.state = sqState.empty
        def setState(self, state:sqState):
            self.state = state
       
        

    def __init__(self) -> None:
        self.x, self.y = instellingen["board_size"]
        self.arraylength = self.x * self.y
        # print(self.arraylength)
        self.bord1D = [None for i in range(self.arraylength)]
        self.board2D = [[None for i in range(self.x)] for j in range(self.y)]
        self.winner = None
        self.populeerCellen()        
        self.geschiedenis = Stapel()
        self.toekomst = Stapel()


    def getCellState(self, ix):
        return self.bord1D[ix].state

    def getCellState2D(self, x,y):
        return self.board2D[y][x].state

    def getBordState(self):
        return [cell.state for cell in self.bord1D]
    
    def zetOpHetBord(self, state):
        for ix in range(len(self.bord1D)):
            self.bord1D[ix].setState(state[ix])
    
    def populeerCellen(self):
        for j in range(self.y):
            for i in range(self.x):
                cell = self.Cell()
                self.bord1D[(j*self.x) + i] = cell
                self.board2D[j][i] = cell
    
    def setLeegState(self):
        for cell in self.bord1D:
            cell.setLeeg()
           
    def setStartState(self):
        self.setLeegState()
        for i in [0,1,self.x,self.x+1]:
            self.bord1D[i].setState(sqState.P1)
            self.bord1D[self.arraylength-1-i].setState(sqState.P2)

    def setBijnaKlaarState(self):
        self.setStartState()
        for row in self.board2D:
            for cell in range(len(row)-2):
                row[cell].setState(sqState.P1)

    def setCellState(self, ix, state):
        self.bord1D[ix].setState(state)

    def vindBuren(self, x, y):
        if x < 0 and x >= self.x and y < 0 and y >= self.y:
            raise indexOutOfBoundException()
        res = []
        difs = [(-1,-1),(0,-1),(+1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)] 
        
        for dx, dy in difs:
            nx = x + dx
            ny = y + dy
            if nx >= 0 and nx < self.x and ny >= 0 and ny < self.y:
                res.append((nx,ny))

        return res
    
    def vindSpringBuren(self, x, y):
        if x < 0 and x >= self.x and y < 0 and y >= self.y:
            raise indexOutOfBoundException()
        difs = [(-2,-2),(0,-2),(+2,-2),(-2,0),(2,0),(-2,2),(0,2),(2,2)] 
        res = []
        
        for dx, dy in difs:
            nx = x + dx
            ny = y + dy
            if nx >= 0 and nx < self.x and ny >= 0 and ny < self.y:
                res.append((nx,ny))
        return res
    
    
    def vindMijnVierkanten(self, team: sqState):
        res = []
        for i in range(self.x):
            for j in range(self.y):
                if self.board2D[j][i].state == team:
                    res.append((i,j))
        return res


    def vindLegaleLoopjes(self, x, y):
        if self.board2D[y][x].state == sqState.empty:
            raise Exception("Cannot make move from empty square!")

        return [(i,j) for i,j in self.vindBuren(x,y) if self.getCellState2D(i,j) == sqState.empty]

    def vindLegaleSprongen(self, x, y):
        if self.board2D[y][x].state == sqState.empty:
            raise Exception("Cannot make move from empty square!")

        # print(f"legalJumps: {[(i,j) for i,j in self.findJumpNeighbours(x,y) if self.getCellState2D(i,j) == sqState.empty]}")
        return [(i,j) for i,j in self.vindSpringBuren(x,y) if self.getCellState2D(i,j) == sqState.empty]
    
    def neemZetTerug(self):
        if not self.geschiedenis.isLeeg():
            huidigeState = self.geschiedenis.trek()
            self.zetOpHetBord(huidigeState)
            self.toekomst.duw(huidigeState)
    def doZetWeer(self):
        print("redo")
        if not self.toekomst.isLeeg():
            huidigeState = self.toekomst.trek()
            self.zetOpHetBord(huidigeState)
            self.geschiedenis.duw(huidigeState)
    
    def doeZet(self, team, mVan, mNaar):
        self.geschiedenis.duw(self.getBordState())
        self.bord1D[mNaar].setState(team)
        x, y = converteerCoordinaten2D(mNaar)
        buren = self.vindBuren(x,y)
        if converteerCoordinaten2D(mVan) not in self.vindBuren(x,y):
            # print(f"{self.findNeighbours(x,y) = }{mFrom = }")
            self.setCellState(mVan, sqState.empty)
        for nx, ny in buren:
            if self.getCellState2D(nx,ny) == andereTeam(team):
                self.setCellState(converteerCoordinaten1D(nx,ny),team)
            # print(n)
        self.toekomst = Stapel()
        self.spelAfgelopen()

    def spelAfgelopen(self):
        p1, p2 = self.getScores()
        if p1 == 0:
            print("P1 Won")
            self.winner = sqState.P2
            return True
        if p2 == 0:
            print("P2 Won")
            self.winner = sqState.P1
            return True
        
        volBord = self.checkVolBord()
        team1HasMove = self.checkTeamHeeftLegaleZet(sqState.P1)
        team2HasMove = self.checkTeamHeeftLegaleZet(sqState.P2)
        p1, p2 = self.getScores()
        self.telScores()
        if volBord:
            return True
        if not team1HasMove:
            print("P1 has no legal moves")
            return True
        if not team2HasMove:
            print("P2 has no legal moves")
            return True

        # print(f"{fullBoard = }, {team1HasMove = }, {team2HasMove = }")


    def telScores(self):
        p1, p2 = self.getScores()
        if p1 > p2:
            self.winner = sqState.P1
        else:
            self.winner = sqState.P2

    def checkTeamHeeftLegaleZet(self, team):
        x, y= instellingen["board_size"]
        for j in range(y):
            for i in range(x):
                if self.getCellState2D(i,j) == team:
                    if len(self.vindLegaleLoopjes(i,j)) > 0 or len(self.vindLegaleSprongen(i,j)) > 0:
                        return True
        return False
        
    def checkVolBord(self):
        for ix in range(len(self.bord1D)):
            if self.getCellState(ix) == sqState.empty:
                return False
        return True
    
    def getScores(self):
        p1 = 0
        p2 = 0
        for cell in self.bord1D:
            if cell.state == sqState.P1: p1 += 1
            if cell.state == sqState.P2: p2 += 1
        return p1, p2
                


    def print1D(self):
        print("board 1D")
        for row in range(self.y):
            print([self.bord1D[cell+(row*self.x)].state.value for cell in range(self.x)])


    def print2D(self):
        print("board 2D")
        for row in range(self.y):
            print([self.board2D[row][cell].state.value for cell in range(self.x)])



    

        
