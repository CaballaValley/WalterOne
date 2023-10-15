import datetime

from walterplayers.constants import Action
from walterplayers.base_player import BasePlayer
from walterplayers.bipolar.strategy_manager import StrategyManager
from walterplayers.bipolar.advisers.defensive_adviser import DefensiveAdviser
from walterplayers.bipolar.advisers.offensive_adviser import OffensiveAdviser
from walterplayers.bipolar.constants import AdviserMode

class BipolarPlayer(BasePlayer):
    ''' Bipolar player will change strategy based on life points.
    If life point is lower than a configured limit, the strategy will be defensive.
    Otherwise Bipolar will be offensive. 
    
    Defensive strategy will look for the health zone using dijkstra to compute the shortest way.
    Offensive strategy will attack when the player find an enemy in a zone.'''

    def __init__(self, defensive_limit=0.8, offensive_limit=0.9, host=None, username=None,
                 password=None, match=None):
        super().__init__(host, username, password, match)
        self._strategy_manager = StrategyManager(defensive_limit, offensive_limit)
        self._advisers = {
            AdviserMode.Defensive: DefensiveAdviser(self),
            AdviserMode.Offensive: OffensiveAdviser(self)}

    def choose_action(self, find_response):
        print(str(datetime.datetime.now()) +
            ' - Updating life point to ' + str(find_response.status.life))

        self._strategy_manager.update_life_points(find_response.status.life)

        if self._strategy_manager.is_strategy_changed():
            print(str(datetime.datetime.now()) +
                ' - Update defends mode with: ' +
                str(AdviserMode.Defensive == self._strategy_manager.get_adviser_mode()))

            self._walterone_client.defends(
                self._match_ia, AdviserMode.Defensive == self._strategy_manager.get_adviser_mode())

        for adviser in self._advisers.values():
            if self._strategy_manager.is_strategy_changed():
                adviser.reset_strategy()
            adviser.add_or_update_zone(find_response)

        print(str(datetime.datetime.now()) +
            ' - Select next action from Adviser: ' +
            str(self._strategy_manager.get_adviser_mode()))

        action = self._advisers[
            self._strategy_manager.get_adviser_mode()].get_next_action(find_response)
        return action

    def update_result(self, executed_action, error, response):
        super().update_result(executed_action, error, response)
        # if an error was raised while moving, we should remove the zone
        if (error
            and Action.MOVE == executed_action
            and response):
            for adviser in self._advisers.values():
                adviser.remove_zone(response.to_zone)
