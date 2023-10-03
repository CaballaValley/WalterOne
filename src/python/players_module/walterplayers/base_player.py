import datetime

from walterplayers.constants import Action
from walterplayers.constants import Role
from walterplayers.client.walterone_client import WalteroneClient

class BasePlayer:
    ''' Abstract player with generic behavior of walterone player '''

    def __init__(self, host=None, username=None, password=None, match=None):
        self._walterone_client = WalteroneClient(host, username, password, match)
        self._life_points = self._match_ia = self._role = None

    def run(self):
        ''' Main method to simulate turn of players. '''
        while True:
            error, find_response = self._walterone_client.find_current_zone()

            if error:
                continue

            self._life_points = find_response.status.life
            self._match_ia = find_response.status.match_ia
            self._role = find_response.status.role

            if self._life_points <= 0:
                # Bad luck, you are died!
                break

            next_action, arg = self.choose_action(find_response)

            print(str(datetime.datetime.now()) +
                " - Executing Action: " + str(next_action) + " with arguments: " + str(arg))

            match next_action:
                case Action.STOP:
                    self.update_result(Action.STOP, False, None)
                    continue
                case Action.ATTACK:
                    error, attack_response = self._walterone_client.attack(arg)
                    self.update_result(Action.ATTACK, error, attack_response)
                    continue
                case Action.DEFEND:
                    error, defend_response = self._walterone_client.defends(self._match_ia, arg)
                    self.update_result(Action.DEFEND, error, defend_response)
                    continue
                case Action.MOVE:
                    error, move_response = self._walterone_client.move_to_zone(arg)
                    self.update_result(Action.MOVE, error, move_response)
                    continue
                case _:
                    print(str(datetime.datetime.now()) +
                        ' - Unknown chosen action: ' + str(next_action))

        print(str(datetime.datetime.now()) + ' - It seems I am died ! :( ')

    def _get_enemies_in_zone(self, zone):
        if Role.BERGEN_TOY == self._role:
            return list(filter(lambda ia: Role.PLAYER == ia.role, zone.ias))

        return zone.ias

    def get_num_enemies_in_zone(self, zone):
        ''' Given a zone, num of enemies in this zone will be returned '''
        return len(self._get_enemies_in_zone(zone))

    def is_possible_attack(self, find_response):
        ''' Return True if there is any anemy to attack in current zone. '''
        return self.get_num_enemies_in_zone(find_response.current_zone) != 0

    def get_enemies(self, find_response):
        ''' Return all enemies in current zone. '''
        return self._get_enemies_in_zone(find_response.current_zone)

    def get_id_ias(self, find_response):
        ''' Return all enemies ids in current zone. '''
        return list(map(lambda ia: ia.id, self._get_enemies_in_zone(find_response.current_zone)))

    def is_possible_move(self, find_response):
        ''' Return True if there is any neighbours zone. '''
        return len(find_response.neighbours_zones) != 0

    def get_id_neighbours_zones(self, find_response):
        ''' Return id for neighbours zones. '''
        return list(map(lambda zone: zone.zone_id, find_response.neighbours_zones))

    def choose_action(self, find_response):
        ''' Delegate logic to choose an action from a find_response
        which is the current status of the player. '''

        raise NotImplementedError()

    def update_result(self, executed_action, error, response):
        ''' After taking an action, this method will be invoked.
        It could be used to update player status with response. '''
        #By default this method only logs the response.
        print(str(datetime.datetime.now()) +
            " - Executed Action: " + str(executed_action) +
            ", Error: " + str(error) + ", Response: " + str(response))
