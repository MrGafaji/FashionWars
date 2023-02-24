import sys
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QMainWindow, QMenuBar, QMenu, QGridLayout, QWidget, QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QAction, QTabWidget, QTabBar, QScrollArea
from PyQt5.QtGui import QFont, QIcon, QTextCursor
from PyQt5.QtCore import Qt
from Vierkant import Square
from GameMachine import Machine, sqState
from instellingen import instellingen
from bruikbaarheden import *
from stapel import Stapel





class GewonnenWidget(QDialog):
    def __init__(self, winner, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.setFixedSize(300,200)


        label = QLabel(f"Player {winner.name} has won!" )
        label.setStyleSheet("font-size: 30px; font-weight:bold;")
        self.layout.addWidget(label)

        resetBtn = QPushButton("New Game")
        resetBtn.clicked.connect(self.accept)
        self.layout.addWidget(resetBtn)
