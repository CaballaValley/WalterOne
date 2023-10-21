from random import choice, uniform

from walterplayers.bipolar.advisers.adviser import Adviser
from walterplayers.constants import Action

class OffensiveAdviser(Adviser):
    ''' Offensive Adviser will be used when life is higher than the limit.
    This Adviser will priorize going for go_ryu zones'''

    def __init__(self, player):
        super().__init__(player)
        self._last_action = Action.STOP

    def is_interesting_zone(self, zone):
        return zone.triggers.go_ryu

    def get_weight_for_zone(self, zone):
        # lets include the edge, taking path with lucky_unlucky
        if zone.triggers.lucky_unlucky:
            weight = 0.5
        else:
            weight = 1
        return weight

    def get_next_action(self, find_response):
        if Action.MOVE == self._last_action and self._player.is_possible_attack(find_response):
            self._last_action = Action.ATTACK
            return (Action.ATTACK, self.get_weakest_enemy(find_response))

        self._last_action = Action.MOVE

        if not self._player.is_possible_move(find_response):
            return Action.STOP, None

        # There is alredy a plan, let execute next step or
        # If a go ryu zone is known, player must go there
        if self._actions_to_execute:
            return self._actions_to_execute.popleft()

        if (find_response.status.buff.go_ryu == 0 and
            self.check_and_update_interested_zone_path(find_response)):
            return self._actions_to_execute.popleft()

        if self._player.is_possible_attack(find_response) and uniform(0,1) <= 0.6:
            return Action.STOP, None

        unkown_zones = self.get_unknown_zones(find_response)

        if unkown_zones:
            return (Action.MOVE, self._get_zone_with_more_enemies(unkown_zones))

        #lets include current zone to the neighbours to be able
        # to stay in the same zone
        possible_zones = find_response.neighbours_zones.copy()
        possible_zones.append(find_response.current_zone)

        zone_with_more_enemies = self._get_zone_with_more_enemies(possible_zones)

        if zone_with_more_enemies == find_response.current_zone.zone_id:
            return (Action.STOP, None)

        return (Action.MOVE, zone_with_more_enemies)

    def _get_zone_with_more_enemies(self, find_response):
        max_enemies = -1
        zones_to_move = []

        for zone in find_response:
            num_enemies = self._player.get_num_enemies_in_zone(zone)
            if num_enemies == max_enemies:
                zones_to_move.append(zone.zone_id)
            elif num_enemies > max_enemies:
                zones_to_move.clear()
                zones_to_move.append(zone.zone_id)
                max_enemies = num_enemies

        return choice(zones_to_move)
