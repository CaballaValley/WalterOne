
from random import choice, uniform

from walterplayers.bipolar.advisers.adviser import Adviser 
from walterplayers.constants import Action

class OffensiveAdviser(Adviser):

    def __init__(self):
        super().__init__()
        self._last_action = Action.Stop

    def is_interesting_zone(self, zone):
        return zone.triggers.go_ryu

    def get_weight_for_zone(self, zone):
        # lets include the edge, taking path with lucky_unlucky
        if zone.triggers.lucky_unlucky:
            weight = 0.5
        else:
            weight = 1

    def get_next_action(self, find_response):
        if Action.Move == self._last_action and len(find_response.current_zone.ias) != 0:
            enemy_to_attack = self.get_weakest_enemy(find_response)
            self._last_action = Action.Attack
            return (Action.Attack, enemy_to_attack)
        
        self._last_action = Action.Move

        #There is alredy a plan, let execute next step
        if self._actions_to_execute:
            return self._actions_to_execute.popleft()
        
        # If a go ryu zone is known, player must go there
        if self.check_and_update_interested_zone_path(find_response):
            print('New path set to go to a go ryu zone')
            return self._actions_to_execute.popleft()
        
        if len(find_response.neighbours_zones) == 0:
            return Action.Stop, None
        
        if len(find_response.current_zone.ias) != 0 and uniform(0,1) >= 0.5:
            return Action.Stop, None

        if uniform(0,1) >= 0.5:
            #sometime go for fight
            possible_zones = self.get_unkown_zones_or_copy(find_response)
            
            return (Action.Move, self._get_zone_with_more_enemies(possible_zones))
        else:
            #sometime explore new zones
            return (Action.Move, self._get_zone_with_more_enemies(find_response.neighbours_zones))    

    def _get_zone_with_more_enemies(self, find_response):
        max_enemies = -1
        zones_to_move = []

        for zone in find_response:
            num_enemies = len(zone.ias)
            if num_enemies >= max_enemies:
                zones_to_move.append(zone.zone_id)
                max_enemies = num_enemies

        return choice(zones_to_move)

