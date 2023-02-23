from PyQt5.QtWidgets import QPushButton, QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize
from settings import settings
import sys

class Square(QPushButton):
    def __init__(self, action, ixBtn, parent=None):
        super().__init__()
        self.state = 0
        self.index = ixBtn
        self.action = action
        self.clicked.connect(self.clickedInGame)
        self.setupUI()


    def setupUI(self):
        self.icons = [QIcon(),QIcon("icons/icons8-hoodie-blue.png"),QIcon("icons/icons8-hoodie-red.png")]
        self.setIcon(self.icons[0])
        self.setIconSize(QSize(settings["icon_size"],settings["icon_size"]))
        self.setFixedSize(settings["btn_size"],settings["btn_size"])


    def setState(self, state = None):
        if state: #set state
            self.state = state
        else: #increment state
            self.state = (self.state+1)%3
        self.setIcon(self.icons[self.state.value])


    def clickedInGame(self):
        self.action(self.index)

    def paintGreen(self):
        self.setStyleSheet("background: green")

    def paintBlue(self):
        self.setStyleSheet("background: blue")
    
    def repaint(self):
        self.setStyleSheet("")

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Square(lambda:0,parent=None)
    with open('style.css') as f:
        style = f.read()
    win.setStyleSheet(style)
    # win.setFixedSize(600,600)
    win.show()
    app.exec_()










