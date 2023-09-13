from base_player import BasePlayer
from constants import Action
from random import choice

class DrunkPlayer(BasePlayer):
    ''' Drunk player will choose one random available action  '''

    def choose_action(self, find_response):
        available_actions = list(Action)

        if not self.is_possible_attack(find_response):
            available_actions.remove(Action.Attack)
        
        if not self.is_possible_move(find_response):
            available_actions.remove(Action.Move)

        result_action = choice(available_actions)

        match result_action:
            case Action.Attack:
                return result_action, choice(find_response.ias)
            case Action.Defend:
                return result_action, choice([True, False])
            case Action.Move:
                return result_action, choice(find_response.neighbours_zones)
            case _:
                return result_action, None