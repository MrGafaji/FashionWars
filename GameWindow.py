import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QMenu, QGridLayout, QWidget, QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QAction, QTabWidget, QTabBar, QScrollArea
from PyQt5.QtGui import QFont, QIcon, QTextCursor
from PyQt5.QtCore import Qt
from Square import Square
from GameEngine import Engine
from settings import settings
from utils import *
from Stack import Stack
from WonWidget import WonWidget
from startMenu import startWidget
from Computer import Computer





class BoardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0,0,0,0)
        self.currentTeam = sqState.P1
        self.engine = Engine()
        self.engine.setStartingState()
        self.makeBoard()
        self.updateBoardState()
        self.stage = stage.SelectFrom
        self.playfrom = None
        self.possibleMoves = []
        self.history = Stack()
        if startWidget().exec_():
            self.secondPlayer = player.human
        else:
            self.secondPlayer = player.computer
            self.computer = Computer(sqState.P2)


    def resetGame(self):
        self.engine = Engine()
        self.engine.setStartingState()
        self.updateBoardState()
        self.currentTeam = sqState.P1

    def checkFinished(self):
        if self.engine.gameFinished():
            if WonWidget(self.engine.winner).exec_():
                self.resetGame()

    def nextTurn(self):
        if self.currentTeam == sqState.P1:
            self.currentTeam = sqState.P2
            if self.secondPlayer == player.computer and self.engine.checkTeamHasLegalMove(sqState.P2):
                mFrom, mTo = self.computer.play(self.engine.getBoardState())
                self.engine.makeMove(sqState.P2, mFrom, mTo)
                self.updateBoardState()
                
                self.board1D[mFrom].paintGreen()
                self.board1D[mTo].paintBlue()
                self.checkFinished()
                self.currentTeam = sqState.P1
                
        else:
            self.currentTeam = sqState.P1

            
        
    def clickedInGame(self,ixBtn):
        self.repaintBoard()
        if self.engine.getCellState(ixBtn) == self.currentTeam and self.stage == stage.SelectFrom:
            self.handleSelectFrom(ixBtn) 

        elif convertCoordinates2D(ixBtn) in self.possibleMoves and self.stage == stage.SelectTo:
            self.engine.makeMove(self.currentTeam, self.playfrom, ixBtn)
            self.updateBoardState()
            self.stage = stage.SelectFrom
            self.nextTurn()

        else:
            self.possibleMoves = []
            self.stage = stage.SelectFrom
            print(f"Wrong turn!")

        self.checkFinished()
            

 

    def handleSelectFrom(self, ixBtn):
        self.updateBoardState() #TODO remove
        self.playfrom = self.board1D[ixBtn]
        self.playfrom.paintGreen()
        x,y = convertCoordinates2D(ixBtn)
        self.possibleMoves = self.engine.findLegalWalks( x,y )
        self.possibleMoves += self.engine.findLegalJumps( x,y )

        self.playfrom = ixBtn
        for xy in self.possibleMoves:
            x,y = xy[0], xy[1]
            self.board[y][x].paintBlue()    
        self.stage = stage.SelectTo   
                
    def repaintBoard(self):
        for sq in self.board1D:
            sq.repaint()

    def makeBoard(self):
        self.board = []
        self.board1D = []
        self.x, y = settings["board_size"]
        for j in range(y):
            row = []
            for i in range(self.x):
                sq = Square(self.clickedInGame, j*self.x+i)  
                self.grid.addWidget(sq, j, i)
                self.board1D.append(sq)
                row.append(sq)
            self.board.append(row)


    def updateBoardState(self):
        self.engine.print1D()
        for i in range(len(self.board1D)):
            enginState = self.engine.getCellState(i)
            self.board1D[i].setState(enginState)



    # def enableTeam(self, team:sqState):
    #     # for square in self.board1D:
    #     #     square.setEnabled(False)
    #     state = self.engine.getBoardState()
    #     for index in range(len(state)):
    #         if state[index] == team:
    #             self.board1D[index].setEnabled(True)

    def squareClicked(self, index):
        pass

    def test(self):
        print("hoi")

class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  
        self.layout = QGridLayout(self)
        self.Board = BoardWidget()
        self.layout.addWidget(self.Board,0,0)
        btn = QPushButton("klick")
        btn.clicked.connect(self.Board.test)
        self.layout.addWidget(btn,1,0)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWid = GameWidget()
        self.setCentralWidget(self.mainWid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(parent=None)
    with open('style.css') as f:
        style = f.read()
    win.setStyleSheet(style)
    # win.setFixedSize(600,600)
    win.show()
    app.exec_()
