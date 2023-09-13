from base_player import BasePlayer
from constants import Action
from random import choice

class JohnnyWalkerPlayer(BasePlayer):
    ''' Jonhy Walker player will be walking and attack if there is an IA in the same zone '''

    def __init__(self, life_points = 200, host = None, username = None, password = None, match = None):
        super().__init__(life_points, host, username, password, match)
        self._last_action = Action.Move


    def choose_action(self, find_response):
        if Action.Move == self._last_action and self.is_possible_attack(find_response):
            # last time jonnhy changed his possition, lets attack if it is possible.
            self._last_action = Action.Attack
            return Action.Attack, choice(find_response.ias)

        if self.is_possible_move(find_response):
            self._last_action = Action.Move
            return Action.Move, choice(find_response.neighbours_zones)    
        else:
            # It wasnt possible to attack neither move.... so he cannot do anything
            self._last_action = Action.Stop
            return Action.Stop, None