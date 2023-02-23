import sys
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QMainWindow, QMenuBar, QMenu, QGridLayout, QWidget, QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QAction, QTabWidget, QTabBar, QScrollArea
from PyQt5.QtGui import QFont, QIcon, QTextCursor
from PyQt5.QtCore import Qt
from Square import Square
from GameEngine import Engine, sqState
from settings import settings
from utils import *
from Stack import Stack





class startWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setWindowFlag(Qt.FramelessWindowHint)


        self.setFixedSize(300,200)
        label = QLabel(f"Fashion Chess" )
        label.setStyleSheet("font-size: 30px; color: red;")
        self.layout.addWidget(label)

        resetBtn = QPushButton("Play agains human")
        resetBtn.clicked.connect(self.accept)
        self.layout.addWidget(resetBtn)

        resetBtn = QPushButton("Play agains computer")
        resetBtn.clicked.connect(self.reject)
        self.layout.addWidget(resetBtn)
