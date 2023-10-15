from random import choice

from walterplayers.base_player import BasePlayer
from walterplayers.constants import Action

class RoadRunnerPlayer(BasePlayer):
    ''' Road Runner beh beh! This player will be always running through the match '''

    def choose_action(self, find_response):
        if self.is_possible_move(find_response):
            return Action.MOVE, choice(self.get_id_neighbours_zones(find_response))

        return Action.STOP, None
