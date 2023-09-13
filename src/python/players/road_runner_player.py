from base_player import BasePlayer
from constants import Action
from random import choice

class RoadRunnerPlayer(BasePlayer):
    ''' Road Runner beh beh! This player will be always running through the match '''

    def choose_action(self, find_response):
        if self.is_possible_move(find_response):
            return Action.Move, choice(find_response.neighbours_zones)
        else:
            return Action.Stop, None