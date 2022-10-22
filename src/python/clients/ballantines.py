from os import getenv
from random import choice

import requests


class IA:

    def __init__(self, host, username, password, match):
        self.walterone_host = getenv("WALTERONE_HOST", "http://localhost:8000")
        self.walterone_username = getenv("WALTERONE_USERNAME", "randolphcarter")
        self.walterone_password = getenv("WALTERONE_PASSWORD", "RandomPassword")
        self.walterone_match = getenv("WALTERONE_MATCH", "2")

        self.auth = (self.walterone_username, self.walterone_password)

        self.move_endpoint = f"{self.walterone_host}/moves/"
        self.find_endpoint = f"{self.walterone_host}/finds/?match={self.walterone_match}"
        self.attack_endpoint = f"{self.walterone_host}/attacks/"

    def attack(self, ias):
        if ias:
            data = {
                "match": self.walterone_match,
                "attack_to": choice(ias)
            }
            response = requests.post(self.attack_endpoint, auth=self.auth, data=data)
            if response.status_code == 400:
                print(response.content)
            print(response.json())

    def find_zone(self):
        response_find = requests.get(self.find_endpoint, auth=self.auth)
        find_data = response_find.json()
        self.attack(find_data['ias'])
        print(find_data)
        return find_data['neighbours_zones']

    def move_to_zone(self):
        data = {
            "match": self.walterone_match,
            "to_zone": choice(self.find_zone())
        }
        response = requests.post(self.move_endpoint, auth=self.auth, data=data)
        print(response.json())
        return response.status_code

    def main(self):
        while self.move_to_zone() == 201:
            pass


if __name__ == "__main__":
    my_ia = IA()
    my_ia.main()
