from constants import Action
from walterplayers.client.walterone_client import WalteroneClient

import datetime

class BasePlayer:
    ''' Abstract player with generic behavior of walterone player '''

    def __init__(self, host = None, username = None, password = None, match = None):
        self._walteroneClient = WalteroneClient(host, username, password, match)

    def run(self):
        while True:
            error, find_response = self._walteroneClient.find_current_zone()

            if error:
                continue

            self._life_points = find_response.current_status.life
            self._match_ia = find_response.current_status.match_ia

            if self._life_points <= 0:
                # Bad luck, you are died!
                break
            
            next_action, arg = self.choose_action(find_response)
            
            match next_action:
                case Action.Stop:
                    self.update_result(Action.Stop, False, None)
                    continue
                case Action.Attack:
                    error, attack_response = self._walteroneClient.attack(arg)
                    self.update_result(Action.Attack, error, attack_response)
                    continue
                case Action.Defend:
                    error, defend_response = self._walteroneClient.defends(self._match_ia, arg)
                    self.update_result(Action.Defend, error, defend_response)
                    continue
                case Action.Move:
                    error, move_response = self._walteroneClient.move_to_zone(arg)
                    self.update_result(Action.Move, error, move_response)
                    continue
                case _:
                    print('Unknown chosen action: ' + str(next_action))

        print('It seems I am died ! :( ')
    
    def _get_walterone_client(self):
        return self._walteroneClient

    def is_possible_attack(self, find_response):
        return len(find_response.ias) != 0
    
    def is_possible_move(self, find_response):
        return len(find_response.neighbours_zones) != 0
            
    def choose_action(self, find_response):
        raise NotImplementedError()

    def update_result(self, executed_action, error, response):
        #By default this method only logs the response.
        print(str(datetime.datetime.now()) + " - Executed Action: " + str(executed_action) + ", Error: " + str(error) + ", Response: " + str(response))



# Estado del juego -> la información que tengo del find_zone con mis vecinos
#
# Funcion heurística -> En base a:
#   - mi vida
#   - la vida de los demás, si mato a alguien
#   - Cercanía de las casillas de vida ->  a menos vida más vale esto
#   - Cercanía de las casillas de bufos ->  a más vida más vale esto
#
# 

