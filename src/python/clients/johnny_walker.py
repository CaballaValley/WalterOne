from os import getenv
from random import choice
from time import sleep

import requests



walterone_host = getenv("WALTERONE_HOST", "http://localhost:8000")
walterone_username = getenv("WALTERONE_USERNAME", "randolphcarter")
walterone_password = getenv("WALTERONE_PASSWORD", "RandomPassword")
walterone_match = getenv("WALTERONE_MATCH", "1")

move_endpoint = f"{walterone_host}/moves/"
auth = (walterone_username, walterone_password)
print(auth)
find_endpoint = f"{walterone_host}/finds/?match={walterone_match}"
response_find = requests.get(find_endpoint, auth=auth)
find_data = response_find.json()
neighbours = find_data['neighbours_zones']

data = {
    "match": walterone_match,
    "to_zone": choice(neighbours)
}

print(data)

response = requests.post(move_endpoint, auth=auth, data=data)
while response.status_code == 201:
    response_find = requests.get(find_endpoint, auth=auth)
    find_data = response_find.json()
    ias = find_data['ias']
    neighbours = find_data['neighbours_zones']
    data['to_zone'] = choice(neighbours)
    print(find_data)
    sleep(5)

    response = requests.post(move_endpoint, auth=auth, data=data)


