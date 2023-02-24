from instellingen import instellingen
from enum import Enum

class sqState(Enum):
    empty= 0
    P1=1
    P2=2
class player(Enum):
    human = 0
    computer = 1

class phase(Enum):
    SelectFrom = 0
    SelectTo = 1

class indexOutOfBoundException(Exception):
    pass

def converteerCoordinaten2D( xy):
    breedte,_ = instellingen["board_size"]
    return xy % breedte, xy // breedte

def converteerCoordinaten1D( x, y):
    breedte,_ = instellingen["board_size"]
    return y * breedte + x

def andereTeam(team):
    if team == sqState.P1:
        return sqState.P2
    elif team == sqState.P2:
        return sqState.P1