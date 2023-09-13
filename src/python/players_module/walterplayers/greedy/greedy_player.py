from random import choice
from greedy.health import Health
from greedy.ship_captain import Ship_Captain
from walterone_client import Walterone_Client

print('Starting greedy player')
health = Health()
ship_captain = Ship_Captain()
walterone_client = Walterone_Client()


while not health.am_I_died():
    print('-------> Current Zone: ' + str(ship_captain.get_current_zone()) + ' <-------')

    find_zone_response = walterone_client.find_zone()
    print('Find zone response status code '+ str(find_zone_response.status_code))
    #Controlar exepcion
    if find_zone_response.status_code != 200:
        continue

    find_zone_data = find_zone_response.json()
    
    print('Updating life ponint to ' + str(find_zone_data['life']))
    health.update_life_points(find_zone_data['life'])

    # podemos activar el mode defensa si estamos en modo defensa
    # si estamos en modeo ofensivo desactivamos la defensa
    print('Defending with mode_defensive ' + str(health.is_defensive_mode_active()))
    # TODO comprobar si el defends penaliza en tiempo 
    walterone_client.defends(health.is_defensive_mode_active())


    print('Updating adjacent zones: ' + str(find_zone_data['neighbours_zones']) + '')
    ship_captain.add_zone(find_zone_data['neighbours_zones'], find_zone_data['triggers']['karin_gift'], find_zone_data['triggers']['go_ryu'], find_zone_data['triggers']['lucky_unlucky'])

    if find_zone_data['ias']:
        attack_to = choice(find_zone_data['ias'])
        print('Attacking to ' + str(attack_to))
        attack_response = walterone_client.attack(attack_to)
        if attack_response.status_code != 201:
            continue
    
    #elegir posibles destinos
    # seleccionar el destino mas optimo
    if ship_captain.get_current_zone():
        new_zone = ship_captain.compute_next_zone(health.is_defensive_mode_active())
    else:
        new_zone = choice(find_zone_data['neighbours_zones'])

    if new_zone:
        print('Moving to zone ' + str(new_zone))
        move_response = walterone_client.move_to_zone(new_zone)

        # TODO
        if move_response.status_code == 201:
            ship_captain.update_current_zone(new_zone)
        elif move_response.status_code == 401:
            print('Removing zone ' + str(new_zone))
            ship_captain.remove_zone(new_zone)
    else:
        print('There is no zone to move')
