from base_player import BasePlayer
from constants import Action
from random import choice

class BillyTheKidPlayer(BasePlayer):
    ''' Biily the kid player will be waiting for other player and attack them until the end '''

    def choose_action(self, find_response):

        if self.is_possible_attack(find_response):
            return Action.Attack, choice(self.get_id_ias(find_response))
        else:
            return Action.Stop, None
            