import sys
from random import choice, uniform

from walterplayers.bipolar.advisers.adviser import Adviser 
from walterplayers.constants import Action

class DefensiveAdviser(Adviser):

    def is_interesting_zone(self, zone):
        return zone.triggers.karin_gift

    def get_weight_for_zone(self, zone):
        # lets include the edge, avoiding taking path with lucky_unlucky
        if zone.triggers.lucky_unlucky:
            weight = 1
        else:
            weight = 0.5

    def get_next_action(self, find_response):
        #There is alredy a plan, let execute next step
        if self._actions_to_execute:
            return self._actions_to_execute.popleft()
        
        # If a karin gift is known, player must go there
        if self.check_and_update_interested_zone_path(find_response):
            return self._actions_to_execute.popleft()
        
        # It looks like we are one of the finisher players.
        if len(find_response.neighbours_zones) == 0 and len(find_response.current_zone.ias) != 0:
            return Action.Attack, self.get_weakest_enemy(find_response)
        
        if len(find_response.current_zone.ias) != 0 and uniform(0,1) < 0.20:
            return Action.Attack, self.get_weakest_enemy(find_response)

        if uniform(0,1) >= 0.5:
            possible_zones = self.get_unkown_zones_or_copy(find_response)
            
            return (Action.Move, self._get_zone_with_less_enemies(possible_zones))
        else:
            return (Action.Move, self._get_zone_with_less_enemies(find_response.neighbours_zones))
    
    def _get_zone_with_less_enemies(self, possible_zones):
        min_enemies = sys.maxsize
        zones_to_move = []

        for zone in possible_zones:
            num_enemies = len(zone.ias)
            if num_enemies <= min_enemies:
                zones_to_move.append(zone.zone_id)
                min_enemies = num_enemies

        return choice(zones_to_move)