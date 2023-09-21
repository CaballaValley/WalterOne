
import networkx as nx
from collections import deque
import sys
from random import choice

from walterplayers.bipolar.adviser import Adviser 
from walterplayers.constants import Action

class DefensiveAdviser(Adviser):

    def __init__(self):
        self._graph = nx.Graph()
        self._karin_gift_zones = set()
        self._actions_to_execute = deque()


    def add_or_update_zone(self, find_response):
        current_zone = find_response.current_status.zone
        
        # lets add a new node into our graph
        # if this node already exists, does not matter, graph will avoid it ;)
        self._graph.add_node(current_zone)
        
        # If there is a karin gift in this zone, we will keep in memory
        if find_response.triggers.karin_gift:
            self._karin_gift_zones.add(current_zone)
        elif current_zone in self._karin_gift_zones:
            # If it is not a karin gift zone but we saved it in the past,
            # we have to let it go
            self._karin_gift_zones.remove(current_zone)
        
        for zone in find_response.neighbours_zones:
            self._graph.add_node(zone)

            # lets include the edge, avoiding taking path with lucky_unlucky
            if lucky_unlucky:
                weight = 0.5
            else:
                weight = 1

            self._graph.add_edge(current_node, zone, weight=weight)
            
    def remove_zone(self, zone):
        if self._graph.has_node(zone):
            self._graph.remove_node(zone)
        
        if zone in self._karin_gift_zones:
            self._karin_gift_zones.remove(zone)

    def reset_strategy(self):
        self._actions_to_execute.clear()

    def get_next_action(self, find_response):
        #There is alredy a plan, let execute next step
        if self._actions_to_execute:
            return self._actions_to_execute.popleft()
        
        # If a karin gift is known, player must go there
        if self._check_and_update_karin_gift_path(find_response):
            return self._actions_to_execute.popleft()

        
        
        # seleccionamos de las neighbours_zones las zonas que aún no conocemos y damos preferencia a las zonas que no tengan enemigos
        possible_zones = []
        for zone in find_response.neighbours_zones:
            if self._graph.has_node(zone):
                continue
            possible_zones.append(zone)
        
        if not possible_zones:
            possible_zones = find_response.neighbours_zones.copy()
        
        # TODO selecciona la que menos enemigos tenga
        random_zone = choice(possible_zones)
        return (Action.Move, random_zone)

    def _check_and_update_karin_gift_path(self, find_response):
        shortest_path = self._compute_shortest_path(find_response.current_status.zone, self._karin_gift_zones)
        if shortest_path:
            while shortest_path:
                self._actions_to_execute.append((Action.Move, next_path.pop(0)))
            return True
        
        return False

    def _compute_shortest_path(self, from_zone, wished_zones):
        possible_zones = wished_zones.copy()

        if from_zone in possible_zones:
            possible_zones.remove(from_zone)

        if not possible_zones:
            return None

        #At this point we have zones to move on
        optimal_weight = sys.maxsize
        result_path = None

        for to_zone in possible_zones:
            try:
                path = nx.astar_path(self._graph, from_zone, to_zone)
                path_weight = nx.path_weight(self._graph, path, 'weight')
                if path_weight <= optimal_weight:
                    result_path = path.copy()
                    optimal_weight = path_weight
            except nx.NetworkXNoPath:
                # handle the exception
                print('There is no path from ' + str(from_zone) + ' to ' + str(to_zone))
                # I have no idea what's going on :(
                continue
        
        return result_path
    
    

            


        
