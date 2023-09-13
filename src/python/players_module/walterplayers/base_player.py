from constants import Action
from walterplayers.client.walterone_client import WalteroneClient

import datetime

class BasePlayer:
    ''' Abstract player with generic behavior of walterone player '''

    def __init__(self, life_points = 200, host = None, username = None, password = None, match = None):
        self._walteroneClient = WalteroneClient(host, username, password, match)
        self._life_points = life_points

    
    def run(self):
        ##TODO Podriamos tener una llamada que nos de la zona en la que estoy y la vida que tengo
        ## buena para iniciarme
        while self._life_points > 0:
            
            error, find_response = self._walteroneClient.find_current_zone()

            if error:
                pass

            ##TODO no necesitariamos la vida aquí.. si la sabemos previamente y con los actaques tambien
            self._life_points = find_response.life


            if self._life_points <= 0:
                # Bad luck, you are died!
                pass

            
            next_action, arg = self.choose_action(find_response)
            
            match next_action:
                case Action.Stop:
                    self.update_result(Action.Stop, False, None)
                    pass
                case Action.Attack:
                    error, attack_response = self._walteroneClient.attack(arg)
                    self.update_result(Action.Attack, error, attack_response)
                    pass
                case Action.Defend:
                    error, defend_response = self._walteroneClient.defends(arg)
                    self.update_result(Action.Defend, error, defend_response)
                    pass
                case Action.Move:
                    error, move_response = self._walteroneClient.move_to_zone(arg)
                    self.update_result(Action.Move, error, move_response)
                    pass
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

