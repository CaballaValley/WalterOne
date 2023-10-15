''' The set of constants in walterone. '''
from enum import Enum

class Action(Enum):
    '''Actions a player can take'''
    STOP = 0
    ATTACK = 1
    DEFEND = 2
    MOVE = 3

class Role(str, Enum):
    ''' Roles assigned to a player '''
    BERGEN_TOY = 'BergenToy'
    PLAYER = 'Player'
