from PyQt5.QtWidgets import QPushButton, QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize
from settings import settings
import sys

class Square(QPushButton):
    def __init__(self, action, parent=None):
        super().__init__(parent)
        self.state = 0
        self.icons = [QIcon(),QIcon("icons/icons8-hoodie-blue.png"),QIcon("icons/icons8-hoodie-red.png")]
        self.setIcon(self.icons[0])
        self.setIconSize(QSize(settings["icon_size"],settings["icon_size"]))
        self.setFixedSize(settings["btn_size"],settings["btn_size"])
        self.setStyleSheet("")
        # self.setEnabled(False)
        # self.clicked.connect(self.setState)


    def setState(self, state = None):
        if not state:
            self.state = (self.state+1)%3
        self.setIcon(self.icons[self.state])
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Square(parent=None)
    with open('style.css') as f:
        style = f.read()
    win.setStyleSheet(style)
    # win.setFixedSize(600,600)
    win.show()
    app.exec_()










