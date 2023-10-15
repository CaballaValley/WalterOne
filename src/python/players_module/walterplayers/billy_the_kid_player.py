from random import choice

from walterplayers.base_player import BasePlayer
from walterplayers.constants import Action

class BillyTheKidPlayer(BasePlayer):
    ''' Biily the kid player will be waiting for other player and attack them until the end '''

    def choose_action(self, find_response):
        if self.is_possible_attack(find_response):
            return Action.ATTACK, choice(self.get_id_ias(find_response))

        return Action.STOP, None
            