import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QHBoxLayout, QWidget, QPushButton
from Square import Square
from GameEngine import Engine
from settings import settings
from utils import *
from WonWidget import WonWidget
from startMenu import startWidget
from Computer import Computer





class BoardWidget(QWidget):
    def __init__(self, changeTurnUiAction, resetUiAction, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout(self)
        self.changeTurnUiAction = changeTurnUiAction
        self.resetUiAction = resetUiAction
        self.grid.setContentsMargins(0,0,0,0)
        self.currentTeam = sqState.P1
        self.engine = Engine()
        self.engine.setStartingState()
        self.makeBoard()
        self.updateBoardState()
        self.stage = stage.SelectFrom
        self.playfrom = None
        self.possibleMoves = []
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
        self.resetUiAction()


    def checkFinished(self):
        if self.engine.gameFinished():
            if WonWidget(self.engine.winner).exec_():
                self.resetGame()

    def nextTurn(self):
        if self.currentTeam == sqState.P1:
            self.currentTeam = sqState.P2
            self.changeTurnUiAction()

            if self.secondPlayer == player.computer and self.engine.checkTeamHasLegalMove(sqState.P2):
                mFrom, mTo = self.computer.play(self.engine.getBoardState())
                self.engine.makeMove(sqState.P2, mFrom, mTo)
                self.updateBoardState()
                
                self.board1D[mFrom].paintGreen()
                self.board1D[mTo].paintBlue()
                self.currentTeam = sqState.P1
                self.changeTurnUiAction()
                
            self.checkFinished()
        else:
            self.currentTeam = sqState.P1
            self.changeTurnUiAction()

            
        
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

    def Undo(self):
        if not self.engine.history.isEmpty():
            self.engine.undoLastMove()
            self.currentTeam = otherTeam(self.currentTeam)
            # self.repaintBoard()
            if self.secondPlayer == player.computer:
                self.engine.undoLastMove()
                self.currentTeam = otherTeam(self.currentTeam)
            self.updateBoardState()
            self.repaintBoard()
        else: 
            print("Can't go back!")

    def redo(self):
        if not self.engine.future.isEmpty():
            self.engine.redoLastMove()
            self.currentTeam = otherTeam(self.currentTeam)
            # self.repaintBoard()
            if self.secondPlayer == player.computer:
                self.engine.redoLastMove()
            self.updateBoardState()
            self.repaintBoard()
        else: 
            print("Can't go forward!")


class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  
        self.layout = QGridLayout(self)
        self.Board = BoardWidget(self.changeTurnUi, self.resetUi)
        self.layout.addWidget(self.Board,0,1,2,2)

        undo = QPushButton("↰")
        undo.clicked.connect(self.Board.Undo)
        # undo.setFixedSize(50,50)
        redo = QPushButton("⮡")
        redo.clicked.connect(self.Board.redo)
        # redo.setFixedSize(50,50)
        self.layout.addWidget(undo, 2, 1)
        # self.layout.addWidget(redo, 2, 2)

        # make player icons 
        self.turn = True
        self.p1 = Square(lambda x:None, 0)
        self.p1.setState(sqState.P1)
        self.p2 = Square(lambda x:None, 0)
        self.p2.setState(sqState.P2)
        self.layout.addWidget(self.p1, 0, 0)
        self.layout.addWidget(self.p2, 1, 3)
        self.changeTurnUi()

    def changeTurnUi(self):
        if self.turn:
            self.p1.paintGreen()
            self.p2.repaint()
            self.turn = not self.turn
        else:
            self.p2.paintGreen()
            self.p1.repaint()
            self.turn = not self.turn

    def resetUi(self):
        self.turn = True
        self.changeTurnUi()
        


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
