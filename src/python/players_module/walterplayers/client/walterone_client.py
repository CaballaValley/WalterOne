from os import getenv
from walterplayers.client.dtos.responses import FindResponse, AttackResponse, MoveResponse, DefendResponse

import requests


def check_variable(env_name, value):
    ''' Check if value is None and raise exception if it is '''
    if not getenv(env_name) and not value:
        all_vars = ', '.join([
            WalteroneClient.WALTERONE_HOST,
            WalteroneClient.WALTERONE_USERNAME,
            WalteroneClient.WALTERONE_PASSWORD,
            WalteroneClient.WALTERONE_MATCH
        ])
        raise Exception(f"Environment {env_name} is not defined. All theese "
                        f"variables are required. Please, set these "
                        f"variables {all_vars} in a environment .env file")


class WalteroneClient:
    ''' Generic client to face walterone server '''

    WALTERONE_HOST = "WALTERONE_HOST"
    WALTERONE_USERNAME = "WALTERONE_USERNAME"
    WALTERONE_PASSWORD = "WALTERONE_PASSWORD"
    WALTERONE_MATCH = "WALTERONE_MATCH"

    def __init__(self, host, username, password, match):

        check_variable(self.WALTERONE_HOST, host)
        check_variable(self.WALTERONE_USERNAME, username)
        check_variable(self.WALTERONE_PASSWORD, password)
        check_variable(self.WALTERONE_MATCH, match)

        self._walterone_host = getenv(self.WALTERONE_HOST, host)
        self._walterone_match = getenv(self.WALTERONE_MATCH, match)

        self._walterone_username = getenv(self.WALTERONE_USERNAME, username)
        self._walterone_password = getenv(self.WALTERONE_PASSWORD, password)

        self._auth = (self._walterone_username, self._walterone_password)

        self._move_endpoint = f"http://{self._walterone_host}/moves/"
        self._find_endpoint = f"http://{self._walterone_host}/finds/?match={self._walterone_match}"
        self._attack_endpoint = f"http://{self._walterone_host}/attacks/"
        self._defend_endpoint = f"http://{self._walterone_host}/defends/"

    def find_current_zone(self):
        ''' Method to get information of current zone. 
        This information will be given by a FindResponse'''

        try:
            response = requests.get(self._find_endpoint, auth=self._auth)

            if response.ok:
                return False, FindResponse(**response.json())
            else:
                print('Error while trying to find zone. Exception : ' + response.text)
                return True, None
        except requests.exceptions.RequestException as e:
            print("Error while trying to find zone. ", e)
            return True, None

    def attack(self, ia):
        ''' Method to attack to another ia.
        Parameters
        ----------
        ia : AI id you want to attack
        '''

        data = {
            "match": self._walterone_match,
            "attack_to": ia
        }

        try:
            response = requests.post(self._attack_endpoint, auth=self._auth, data=data)

            if response.ok:
                return False, AttackResponse(**response.json())
            else:
                print('Error while trying to attack to ia ' + str(ia) + '. Exception : ' + response.text)
                return True, None
        except requests.exceptions.RequestException as e:
            print("Error while trying to attack. ", e)
            return True, None

    def move_to_zone(self, to_zone):
        ''' Method to your ia to another zone.
        Parameters
        ----------
        to_zone : Destination of movement.
        '''

        data = {
            "match": self._walterone_match,
            "to_zone": to_zone
        }

        try:
            response = requests.post(self._move_endpoint, auth=self._auth, data=data)

            if response.ok:
                return False, MoveResponse(**response.json())
            else:
                print('Error while trying to move to zone ' + str(to_zone) + '. Exception : ' + response.text)
                return True, None
        except requests.exceptions.RequestException as e:
            print("Error while trying to move. ", e)
            return True, None

    def defends(self, match_ia, active):
        ''' Chanfe your defend mode.
        Parameters
        ----------
        match_ia: Identify of an IA playing in a match.
        active : True if you want to be defensive player, otherwise False.
        '''

        data = {
            "active": active,
            "match_ia": match_ia
        }

        try:
            response = requests.post(self._defend_endpoint, auth=self._auth, data=data)

            if response.ok:
                return False, DefendResponse(**response.json())
            else:
                print('Error while trying to defend with active ' + str(active) + '. Exception : ' + response.text)
                return True, None
        except requests.exceptions.RequestException as e:
            print("Error while trying to defend. ", e)
            return True, None

###### TEST
# client = WalteroneClient("http://127.0.0.1:8000", "jmnieto", "Gu4rma1986", "2")

# error, find = client.find_current_zone()
# print(error)
# print(find.model_dump())

# error, attack = client.attack(9)
# print(error)
# print(attack.model_dump())

# error, move = client.move_to_zone(5)
# print(error)
# print(move)


# error, defend = client.defends(2, False)
# print(error)
# print(defend.model_dump())
