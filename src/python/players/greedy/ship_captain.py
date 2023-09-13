import random
import sys
from greedy.graph_manager import Graph_Manager

class Ship_Captain:
    def __init__(self):
        self._map_zone_to_adjacents = {}
        self._buff_to_zones = {'karim_gift': set(), 'go_ryu': set(), 'lucky_unlucky': set()}
        self._current_zone = None
        self._previous_zone = None
        self._graph_manager = Graph_Manager()
    
    def add_zone(self, adjancent_zones, karim_gift, go_ryu, lucky_unlucky):
        if not self._current_zone:
            return
        
        if karim_gift:
            self._buff_to_zones['karim_gift'].add(self._current_zone)
        
        if go_ryu:
            self._buff_to_zones['go_ryu'].add(self._current_zone)
        
        if lucky_unlucky:
            self._buff_to_zones['lucky_unlucky'].add(self._current_zone)
         
        if self._current_zone not in self._map_zone_to_adjacents:
            self._map_zone_to_adjacents[self._current_zone] = set()
        
        for zone in adjancent_zones:
            self._map_zone_to_adjacents[self._current_zone].add(zone)
            self._graph_manager.add_node(self._current_zone, zone, lucky_unlucky)
    
    def remove_zone(self, zone):
        if zone in self._buff_to_zones['karim_gift']:
            self._buff_to_zones['karim_gift'].remove(zone)
        
        if zone in self._buff_to_zones['go_ryu']:
            self._buff_to_zones['go_ryu'].remove(zone)
        
        if zone in self._buff_to_zones['lucky_unlucky']:
            self._buff_to_zones['lucky_unlucky'].remove(zone)
         
        if zone in self._map_zone_to_adjacents:
            self._map_zone_to_adjacents.pop(zone, None)
            self._graph_manager.remove_node(zone)
        
        for neighbours_zones in self._map_zone_to_adjacents.values():
            if zone in neighbours_zones:
                neighbours_zones.remove(zone)

    def update_current_zone(self, current_zone):
        self._previous_zone = self._current_zone
        self._current_zone = current_zone

    def compute_next_zone(self, defensive_mode):
        possible_destinations = self._choose_destinations(defensive_mode)

        if not possible_destinations:
            return
        
        optimal_weight = sys.maxsize
        result = None

        for destination in possible_destinations:
            path = self._graph_manager.compute_path(self._current_zone, destination, defensive_mode)
            path_weight = self._graph_manager.get_weight(path, defensive_mode)
            if path_weight <= optimal_weight:
                result = path[1]
        
        return result
    
    def _choose_destinations(self, defensive_mode):

        if defensive_mode:
            if self._buff_to_zones['karim_gift']:
                karin_gift_zones_possible = self._buff_to_zones['karim_gift'].copy()
                if self._current_zone in karin_gift_zones_possible:
                    karin_gift_zones_possible.remove(self._current_zone)
                
                if karin_gift_zones_possible:
                    return karin_gift_zones_possible
                else:
                    return self._choose_uknown_adjacents(defensive_mode)
            else:
                return self._choose_uknown_adjacents(defensive_mode)
        else:
            random_value = random.random()
            if random_value >= 0.5:
                return self._choose_uknown_adjacents(defensive_mode)

            if self._buff_to_zones['go_ryu']:
                go_ryu_zones_possible = self._buff_to_zones['go_ryu'].copy()
                if self._current_zone in go_ryu_zones_possible:
                    go_ryu_zones_possible.remove(self._current_zone)
                
                if go_ryu_zones_possible:
                    return go_ryu_zones_possible
                else:
                    return self._choose_uknown_adjacents(defensive_mode)
            else:
                return self._choose_uknown_adjacents(defensive_mode)
    
    def _choose_uknown_adjacents(self, defensive_mode):
        adj_zones_possible = self._map_zone_to_adjacents[self._current_zone].copy()
        for zone in self._map_zone_to_adjacents.keys():
            if zone in adj_zones_possible:
                adj_zones_possible.remove(zone)
        if adj_zones_possible:
            return adj_zones_possible
        else:
            adj_zones_possible = self._map_zone_to_adjacents[self._current_zone].copy()

            if defensive_mode:
                return adj_zones_possible
            
            if self._previous_zone:
                if self._previous_zone in adj_zones_possible:
                    adj_zones_possible.remove(self._previous_zone)
                
                if adj_zones_possible:
                    return adj_zones_possible
                else:
                    return self._map_zone_to_adjacents[self._current_zone].copy()
            
            return adj_zones_possible
            

    def get_map_zone(self):
        return self._map_zone_to_adjacents
    
    def get_current_zone(self):
        return self._current_zone