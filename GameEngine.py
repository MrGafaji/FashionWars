from settings import settings
from utils import *



class Engine():
    class Cell():
        def __init__(self):
            self.state = sqState.empty
        def setEmpty(self):
            self.state = sqState.empty
        def setState(self, state:sqState):
            self.state = state
       
        

    def __init__(self) -> None:
        self.x, self.y = settings["board_size"]
        self.arraylength = self.x * self.y
        # print(self.arraylength)
        self.board1D = [None for i in range(self.arraylength)]
        self.board2D = [[None for i in range(self.x)] for j in range(self.y)]
        self.winner = None
        self.populateCells()

    def getCellState(self, ix):
        return self.board1D[ix].state

    def getCellState2D(self, x,y):
        return self.board2D[y][x].state

    def getBoardState(self):
        return [cell.state for cell in self.board1D]
    
    def setBoardState(self, state):
        for ix in range(len(self.board1D)):
            self.board1D[ix].setState(state[ix])
    
    def populateCells(self):
        for j in range(self.y):
            for i in range(self.x):
                cell = self.Cell()
                self.board1D[(j*self.x) + i] = cell
                self.board2D[j][i] = cell
    
    def setEmptyState(self):
        for cell in self.board1D:
            cell.setEmpty()
           
    def setStartingState(self):
        self.setEmptyState()
        for i in [0,1,self.x,self.x+1]:
            self.board1D[i].setState(sqState.P1)
            self.board1D[self.arraylength-1-i].setState(sqState.P2)

    def setAlmostFinishedState(self):
        self.setStartingState()
        for row in self.board2D:
            for cell in range(len(row)-2):
                row[cell].setState(sqState.P1)


    def setCellState(self, ix, state):
        self.board1D[ix].setState(state)

    def findNeighbours(self, x, y):
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
    
    def findJumpNeighbours(self, x, y):
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
    
    
    def findMySquares(self, team: sqState):
        res = []
        for i in range(self.x):
            for j in range(self.y):
                if self.board2D[j][i].state == team:
                    res.append((i,j))
        return res


    def findLegalWalks(self, x, y):
        if self.board2D[y][x].state == sqState.empty:
            raise Exception("Cannot make move from empty square!")

        return [(i,j) for i,j in self.findNeighbours(x,y) if self.getCellState2D(i,j) == sqState.empty]

    def findLegalJumps(self, x, y):
        if self.board2D[y][x].state == sqState.empty:
            raise Exception("Cannot make move from empty square!")

        # print(f"legalJumps: {[(i,j) for i,j in self.findJumpNeighbours(x,y) if self.getCellState2D(i,j) == sqState.empty]}")
        return [(i,j) for i,j in self.findJumpNeighbours(x,y) if self.getCellState2D(i,j) == sqState.empty]
    
    def makeMove(self, team, mFrom, mTo):
        self.board1D[mTo].setState(team)
        x, y = convertCoordinates2D(mTo)
        neighbours = self.findNeighbours(x,y)
        if convertCoordinates2D(mFrom) not in self.findNeighbours(x,y):
            # print(f"{self.findNeighbours(x,y) = }{mFrom = }")
            self.setCellState(mFrom, sqState.empty)
        for nx, ny in neighbours:
            if self.getCellState2D(nx,ny) == otherTeam(team):
                self.setCellState(convertCoordinates1D(nx,ny),team)
            # print(n)

    def gameFinished(self):
        p1, p2 = self.getScores()
        if p1 == 0:
            print("P1 Won")
            self.winner = sqState.P2
            return True
        if p2 == 0:
            print("P2 Won")
            self.winner = sqState.P1
            return True
        
        fullBoard = self.checkFullBoard()
        team1HasMove = self.checkTeamHasLegalMove(sqState.P1)
        team2HasMove = self.checkTeamHasLegalMove(sqState.P2)
        if fullBoard:
            return True
        if not team1HasMove:
            print("P1 has no legal moves")
            return True
        if not team2HasMove:
            print("P2 has no legal moves")
            return True

        # print(f"{fullBoard = }, {team1HasMove = }, {team2HasMove = }")




    def checkTeamHasLegalMove(self, team):
        board = self.board1D
        x, y= settings["board_size"]
        for j in range(y):
            for i in range(x):
                if self.getCellState2D(i,j) == team:
                    if len(self.findLegalWalks(i,j)) > 0 or len(self.findLegalJumps(i,j)) > 0:
                        return True
        return False
        
    def checkFullBoard(self):
        for ix in range(len(self.board1D)):
            if self.getCellState(ix) == sqState.empty:
                return False
        return True
    
    def getScores(self):
        p1 = 0
        p2 = 0
        for cell in self.board1D:
            if cell.state == sqState.P1: p1 += 1
            if cell.state == sqState.P2: p2 += 1
        return p1, p2
                


    def print1D(self):
        print("board 1D")
        for row in range(self.y):
            print([self.board1D[cell+(row*self.x)].state.value for cell in range(self.x)])


    def print2D(self):
        print("board 2D")
        for row in range(self.y):
            print([self.board2D[row][cell].state.value for cell in range(self.x)])



    

        
