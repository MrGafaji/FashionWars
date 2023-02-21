import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QMenu, QGridLayout, QWidget, QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QAction, QTabWidget, QTabBar, QScrollArea
from PyQt5.QtGui import QFont, QIcon, QTextCursor
from PyQt5.QtCore import Qt
from Square import Square
from GameEngine import Engine, sqState
from settings import settings

class BoardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0,0,0,0)
        self.engine = Engine()
        self.engine.setStartingState()
        self.makeBoard()


    def makeBoard(self):
        self.board = []
        self.board1D = []
        x, y = settings["board_size"]
        for j in range(y):
            row = []
            for i in range(x):
                sq = Square(self.squareClicked)  
                sq.setEnabled(False)             
                self.grid.addWidget(sq, i, j)
                self.board1D.append(sq)
                row.append(sq)
            self.board.append(row)


    def updateBoardState(self):
        for i in range(len(self.board1D)):
            enginState = self.engine.getCellState(i)
            self.board1D[i].setState(enginState)

    def enableTeam(self, team:sqState):
        for square in self.board1D:
            square.setEnabled(False)
        state = self.engine.getBoardState()
        for index in range(len(state)):
            if state[index] == team:
                self.board1D[index].setEnabled(True)

    def squareClicked(self):
        pass

    def test(self):
        pass

class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  
        self.layout = QGridLayout(self)
        self.Board = BoardWidget()
        self.layout.addWidget(self.Board,0,0)
        btn = QPushButton("klick")
        btn.clicked.connect(self.Board.test)
        self.layout.addWidget(BoardWidget(),0,0)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWid = BoardWidget()
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


"""
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QMenu, QGridLayout, QWidget, QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QAction, QTabWidget, QTabBar, QScrollArea
from PyQt5.QtGui import QFont, QIcon, QTextCursor
from PyQt5.QtCore import Qt
from GameButton import GameButton

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0,0,0,0)

        for i in range(7):
            for j in range(7):
                btn = GameButton()               
                self.grid.addWidget(btn, i, j)

class PyPOMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWid = MainWidget()
        self.setCentralWidget(self.mainWid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PyPOMainWindow(parent=None)
    with open('style.css') as f:
        style = f.read()
    win.setStyleSheet(style)
    # win.setFixedSize(600,600)
    win.show()
    app.exec_()
"""