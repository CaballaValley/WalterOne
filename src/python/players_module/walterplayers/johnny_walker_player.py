# python imports
from random import choice
# third party imports
# local imports
from constants import Action
from walterplayers.base_player import BasePlayer


class JohnnyWalkerPlayer(BasePlayer):
    ''' Jonhy Walker player will be walking and attack if there is an IA in the same zone '''

    def __init__(self, host=None, username=None, password=None, match=None):
        super().__init__(host, username, password, match)
        self._last_action = Action.Move

    def choose_action(self, find_response):
        if Action.Move == self._last_action and self.is_possible_attack(find_response):
            # last time jonnhy changed his possition, lets attack if it is possible.
            self._last_action = Action.Attack
            return Action.Attack, choice(self.get_id_ias(find_response))

        if self.is_possible_move(find_response):
            self._last_action = Action.Move
            return Action.Move, choice(self.get_id_neighbours_zones(find_response))
        else:
            # It wasnt possible to attack neither move.... so he cannot do anything
            self._last_action = Action.Stop
            return Action.Stop, None
