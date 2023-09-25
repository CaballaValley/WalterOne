from base_player import BasePlayer
from constants import Action
from random import choice

class RoadRunnerPlayer(BasePlayer):
    ''' Road Runner beh beh! This player will be always running through the match '''

    def choose_action(self, find_response):
        if self.is_possible_move(find_response):
            return Action.Move, choice(self.get_id_neighbours_zones(find_response))
        else:
            return Action.Stop, None