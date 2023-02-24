import sys
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QMainWindow, QMenuBar, QMenu, QGridLayout, QWidget, QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QAction, QTabWidget, QTabBar, QScrollArea
from PyQt5.QtGui import QFont, QIcon, QTextCursor
from PyQt5.QtCore import Qt
from Vierkant import Square
from GameMachine import Machine, sqState
from instellingen import instellingen
from bruikbaarheden import *
from stapel import Stapel





class startWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setWindowFlag(Qt.FramelessWindowHint)


        self.setFixedSize(300,200)
        label = QLabel(f"Mode schaken" )
        label.setStyleSheet("font-size: 30px; color: red;")
        self.layout.addWidget(label)

        resetBtn = QPushButton("Twee spelers")
        resetBtn.clicked.connect(self.accept)
        self.layout.addWidget(resetBtn)

        resetBtn = QPushButton("Speel tegen computer")
        resetBtn.clicked.connect(self.reject)
        self.layout.addWidget(resetBtn)
