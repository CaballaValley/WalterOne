from collections import deque
import sys
import networkx as nx

from walterplayers.constants import Action

class Adviser():
    ''' Adviser for player. An adviser will have:
        - A graph to keep in memory the map where player has been walking for.
        - Interested zones for an adviser
        - Actions to execute.
        - Player '''

    def __init__(self, player):
        self._graph = nx.Graph()
        self._interested_zones = set()
        self._actions_to_execute = deque()
        self._player = player
        self._known_zones = set()

    def add_or_update_zone(self, find_response):
        ''' Method to update zone information into an adviser. '''
        current_zone = find_response.current_zone.zone_id

        # lets add a new node into our graph
        # if this node already exists, does not matter, graph will avoid it ;)
        self._graph.add_node(current_zone)
        self._known_zones.add(current_zone)

        # If adviser is interested on this zone, we will keep in memory
        if self.is_interesting_zone(find_response.current_zone):
            self._interested_zones.add(current_zone)
        elif current_zone in self._interested_zones:
            # If it was interesting zone in the past, we have to let it go
            self._interested_zones.remove(current_zone)

        weight = self.get_weight_for_zone(find_response.current_zone)

        for zone in find_response.neighbours_zones:
            self._graph.add_node(zone.zone_id)
            self._graph.add_edge(current_zone, zone.zone_id, weight=weight)

    def is_interesting_zone(self, zone):
        ''' Method to notice if a zone must be keep in memory. '''
        raise NotImplementedError()

    def get_weight_for_zone(self, zone):
        ''' Method to return weight for a given zone. '''
        raise NotImplementedError()

    def remove_zone(self, zone):
        ''' A zone cuold be remove and this must be notify to an adviser'''
        if self._graph.has_node(zone):
            self._graph.remove_node(zone)

        if zone in self._interested_zones:
            self._interested_zones.remove(zone)

    def reset_strategy(self):
        ''' Reset strategy! Change defensive <-> offensive'''
        self._actions_to_execute.clear()

    def get_next_action(self, find_response):
        ''' Method to compute next action following a strategy by an adviser. '''
        raise NotImplementedError()

    def get_unknown_zones(self, find_response):
        ''' Return unknown zones. If all zones are knwon, return empty list. '''
        return list(filter(
            lambda zone: not zone.zone_id in self._known_zones, find_response.neighbours_zones))


    def get_weakest_enemy(self, find_response):
        ''' The weakest enemy in the current zone. '''
        min_life = sys.maxsize
        enemy_to_attack = None

        for enemy in self._player.get_enemies(find_response):
            if enemy.life <= min_life:
                enemy_to_attack = enemy.id
                min_life = enemy.life

        return enemy_to_attack

    def check_and_update_interested_zone_path(self, find_response):
        ''' Return True if there is a path to an intereted zone. Otherwise False. '''
        shortest_path = self._compute_shortest_path(
            find_response.current_zone.zone_id, self._interested_zones)

        if not shortest_path:
            return False

        if find_response.current_zone.zone_id in shortest_path:
            shortest_path.remove(find_response.current_zone.zone_id)

        for path in shortest_path:
            self._actions_to_execute.append((Action.MOVE, path))

        return True

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
