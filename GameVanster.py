import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QHBoxLayout, QWidget, QPushButton
from Vierkant import Square
from GameMachine import Machine
from instellingen import instellingen
from bruikbaarheden import *
from WinWidget import GewonnenWidget
from startMenu import startWidget
from Computer import Computer





class BoardWidget(QWidget):
    def __init__(self, beurtActie, resetActie, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout(self)
        self.beurtActie = beurtActie
        self.resetActie = resetActie
        self.grid.setContentsMargins(0,0,0,0)
        self.huidigeTeam = sqState.P1
        self.engine = Machine()
        self.engine.setStartState()
        self.maakBord()
        self.updateBordState()
        self.stage = phase.SelectFrom
        self.speelVanuit = None
        self.mogelijkeZetten = []
        if startWidget().exec_():
            self.tweedeSpeler = player.human
        else:
            self.tweedeSpeler = player.computer
            self.computer = Computer(sqState.P2)


    def resetGame(self):
        self.engine = Machine()
        self.engine.setStartState()
        self.updateBordState()
        self.huidigeTeam = sqState.P1
        self.resetActie()


    def checkAfgelopen(self):
        if self.engine.spelAfgelopen():
            if GewonnenWidget(self.engine.winner).exec_():
                self.resetGame()

    def volgendeBeurt(self):
        if self.huidigeTeam == sqState.P1:
            self.huidigeTeam = sqState.P2
            self.beurtActie()

            if self.tweedeSpeler == player.computer and self.engine.checkTeamHeeftLegaleZet(sqState.P2):
                mFrom, mTo = self.computer.speel(self.engine.getBordState())
                self.engine.doeZet(sqState.P2, mFrom, mTo)
                self.updateBordState()
                
                self.bord1D[mFrom].paintGreen()
                self.bord1D[mTo].paintBlue()
                self.huidigeTeam = sqState.P1
                self.beurtActie()
                
            self.checkAfgelopen()
        else:
            self.huidigeTeam = sqState.P1
            self.beurtActie()

            
        
    def clickedInGame(self,ixBtn):
        self.herkleurBord()
        if self.engine.getCellState(ixBtn) == self.huidigeTeam and self.stage == phase.SelectFrom:
            self.handleSelectFrom(ixBtn) 

        elif converteerCoordinaten2D(ixBtn) in self.mogelijkeZetten and self.stage == phase.SelectTo:
            self.engine.doeZet(self.huidigeTeam, self.speelVanuit, ixBtn)
            self.updateBordState()
            self.stage = phase.SelectFrom
            self.volgendeBeurt()

        else:
            self.mogelijkeZetten = []
            self.stage = phase.SelectFrom
            print(f"Wrong turn!")

        self.checkAfgelopen()
            

 

    def handleSelectFrom(self, ixBtn):
        self.updateBordState() #TODO remove
        self.speelVanuit = self.bord1D[ixBtn]
        self.speelVanuit.paintGreen()
        x,y = converteerCoordinaten2D(ixBtn)
        self.mogelijkeZetten = self.engine.vindLegaleLoopjes( x,y )
        self.mogelijkeZetten += self.engine.vindLegaleSprongen( x,y )

        self.speelVanuit = ixBtn
        for xy in self.mogelijkeZetten:
            x,y = xy[0], xy[1]
            self.bord[y][x].paintBlue()    
        self.stage = phase.SelectTo   
                
    def herkleurBord(self):
        for sq in self.bord1D:
            sq.repaint()

    def maakBord(self):
        self.bord = []
        self.bord1D = []
        self.x, y = instellingen["board_size"]
        for j in range(y):
            row = []
            for i in range(self.x):
                sq = Square(self.clickedInGame, j*self.x+i)  
                self.grid.addWidget(sq, j, i)
                self.bord1D.append(sq)
                row.append(sq)
            self.bord.append(row)


    def updateBordState(self):
        self.engine.print1D()
        for i in range(len(self.bord1D)):
            enginState = self.engine.getCellState(i)
            self.bord1D[i].setState(enginState)



    def Undo(self):
        if not self.engine.geschiedenis.isLeeg():
            self.engine.neemZetTerug()
            self.huidigeTeam = andereTeam(self.huidigeTeam)
            # self.repaintBoard()
            if self.tweedeSpeler == player.computer:
                self.engine.neemZetTerug()
                self.huidigeTeam = andereTeam(self.huidigeTeam)
            self.updateBordState()
            self.herkleurBord()
        else: 
            print("Can't go back!")

    def redo(self):
        if not self.engine.toekomst.isLeeg():
            self.engine.doZetWeer()
            self.huidigeTeam = andereTeam(self.huidigeTeam)
            # self.repaintBoard()
            if self.tweedeSpeler == player.computer:
                self.engine.doZetWeer()
            self.updateBordState()
            self.herkleurBord()
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
