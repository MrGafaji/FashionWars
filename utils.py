from settings import settings
from enum import Enum

class sqState(Enum):
    empty= 0
    P1=1
    P2=2

class stage(Enum):
    SelectFrom = 0
    SelectTo = 1

class indexOutOfBoundException(Exception):
    pass

def convertCoordinates2D( xy):
    width,_ = settings["board_size"]
    return xy % width, xy // width

def convertCoordinates1D( x, y):
    width,_ = settings["board_size"]
    return y * width + x

def otherTeam(team):
    if team == sqState.P1:
        return sqState.P2
    elif team == sqState.P2:
        return sqState.P1