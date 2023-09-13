from ..base_player import BasePlayer
from bipolar.strategy_manager import StrategyManager
from bipolar.graph_driver import GraphDriver

import datetime

class BipolarPlayer(BasePlayer):
    ''' Bipolar player will change strategy based on life points.
    If life point is lower than a configured limit, the strategy will be defensive. Otherwise Bipolar will be offensive. 
    
    Defensive strategy will look for the health zone using dijkstra to compute the shortest way.
    Offensive strategy will attack when the player find an enemy in a zone.'''

    def __init__(self, life_points = 200, defensive_limit = 0.8, ofensive_limit = 0.9, host = None, username = None, password = None, match = None):
        super().__init__(life_points, host, username, password, match)
        self._strategy_manager = StrategyManager(life_points, defensive_limit, ofensive_limit)
        self._graph_driver = GraphDriver()


    def choose_action(self, find_response):

        print(str(datetime.datetime.now()) + " - Updating life ponint to " + str(find_response.life))
        self._strategy_manager.update_life_points(find_response.life)


        print('Update defends mode with: ' + str(self._strategy_manager.is_defensive_mode_active()))
        self._get_walterone_client().defends(self._strategy_manager.is_defensive_mode_active())


        #print('Updating adjacent zones: ' + str(find_zone_data['neighbours_zones']) + '')
        #ship_captain.add_zone(find_zone_data['neighbours_zones'], find_zone_data['triggers']['karin_gift'], find_zone_data['triggers']['go_ryu'], find_zone_data['triggers']['lucky_unlucky'])


    
    def update_result(self, executed_action, error, response):
        super().update_result(executed_action, error, response)
        
        # si ha fallado un movimiento es xq ya no existe la zona, tenemos que eliminarla