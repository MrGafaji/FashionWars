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
        self.populateCells()

    def getCellState(self, ix):
        return self.board1D[ix].state

    def getCellState2D(self, x,y):
        return self.board2D[y][x].state

    def getBoardState(self):
        return [cell.state for cell in self.board1D]
    
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


    def findLegalMoves(self, x, y):
        if self.board2D[y][x].state == sqState.empty:
            raise Exception("Cannot make move from empty square!")

        return [(i,j) for i,j in self.findNeighbours(x,y) if self.board2D[j][i].state == sqState.empty]

    def findLegalJumps(self, x, y):
        if self.board2D[y][x].state == sqState.empty:
            raise Exception("Cannot make move from empty square!")

        return [(i,j) for i,j in self.findJumpNeighbours(x,y) if self.board2D[j][i].state == sqState.empty]
    
    def makeMove(self, team, mFrom, mTo):
        self.board1D[mTo].setState(team)
        x, y = convertCoordinates2D(mTo)
        neighbours = self.findNeighbours(x,y)
        if convertCoordinates2D(mFrom) not in self.findNeighbours(x,y):
            print(f"{self.findNeighbours(x,y) = }{mFrom = }")
            self.setCellState(mFrom, sqState.empty)
        for nx, ny in neighbours:
            if self.getCellState2D(nx,ny) == otherTeam(team):
                self.setCellState(convertCoordinates1D(nx,ny),team)
            # print(n)


    def print1D(self):
        print("board 1D")
        for row in range(self.y):
            print([self.board1D[cell+(row*self.x)].state.value for cell in range(self.x)])


    def print2D(self):
        print("board 2D")
        for row in range(self.y):
            print([self.board2D[row][cell].state.value for cell in range(self.x)])



    

        
