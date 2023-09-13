from os import getenv
from walterplayers.client.dtos.responses import FindResponse, AttackResponse, MoveResponse, DefendResponse

import requests


# TODO mover el paquete client fuera del players...no tengo cojones que funcionen los import
class WalteroneClient:
    ''' Generic client to face walterone server '''

    def __init__(self, host, username, password, match):
        self._walterone_host = getenv("WALTERONE_HOST", host)
        self._walterone_username = getenv("WALTERONE_USERNAME", username)
        self._walterone_password = getenv("WALTERONE_PASSWORD", password)
        self._walterone_match = getenv("WALTERONE_MATCH", match)
        # TODO self._walterone_ia = getenv("WALTERONE_MATCH", match)
        self._walterone_ia = 11

        self._auth = (self._walterone_username, self._walterone_password)

        self._move_endpoint = f"{self._walterone_host}/moves/"
        self._find_endpoint = f"{self._walterone_host}/finds/?match={self._walterone_match}"
        self._attack_endpoint = f"{self._walterone_host}/attacks/"
        self._defend_endpoint = f"{self._walterone_host}/defends/"

    def find_current_zone(self):
        ''' Method to get information of current zone. 
        This information will be given by a FindResponse'''

        response = requests.get(self._find_endpoint, auth=self._auth)
        if response.ok:
            return False, FindResponse(**response.json())
        else:
            print('Error while trying to find zone. Exception : ' + response.text)
            return True, None

    def attack(self, ia):
        ''' Method to attack to another ia.
        Parameters
        ----------
        ia : AI id you want to attack
        '''

        # TODO el attack te da la vida de los jugadores anterior al ataque, tiene sentido?
        # No sé si me ha dañado o no :(
        data = {
            "match": self._walterone_match,
            "attack_to": ia
        }

        response = requests.post(self._attack_endpoint, auth=self._auth, data=data)

        if response.ok:
            return False, AttackResponse(**response.json())
        else:
            print('Error while trying to attack to ia ' + str(ia) + '. Exception : ' + response.text)
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

        response = requests.post(self._move_endpoint, auth=self._auth, data=data)

        if response.ok:
            return False, MoveResponse(**response.json())
        else:
            print('Error while trying to move to zone ' + str(to_zone) + '. Exception : ' + response.text)
            return True, None

    def defends(self, active):
        ''' Chanfe your defend mode.
        Parameters
        ----------
        active : True if you want to be defensive player, otherwise False.
        '''

        data = {
            "active": active,
            # TODO cómo obtengo el id de mi IA para defenderme? lo tengo que sacar de un ataque?
            "match_ia": self._walterone_ia
        }

        response = requests.post(self._defend_endpoint, auth=self._auth, data=data)

        if response.ok:
            return False, DefendResponse(**response.json())
        else:
            print('Error while trying to defend with active ' + str(active) + '. Exception : ' + response.text)
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


# error, defend = client.defends(False)
# print(error)
# print(defend.model_dump())
