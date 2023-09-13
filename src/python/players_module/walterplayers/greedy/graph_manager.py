import networkx as nx

class Graph_Manager:
    def __init__(self):
        self._defensive_graph = nx.Graph()
        self._offensive_graph = nx.Graph()

    def add_node(self, current_node, dest_node, lucky_unlucky):
        self._defensive_graph.add_node(current_node)
        self._offensive_graph.add_node(current_node)
        self._defensive_graph.add_node(dest_node)
        self._offensive_graph.add_node(dest_node)        

        if lucky_unlucky:
            weight_def = 0.5
            weight_offen = 1
        else:
            weight_def = 1
            weight_offen = 1.5
                
        self._defensive_graph.add_edge(current_node, dest_node, weight=weight_def)
        self._offensive_graph.add_edge(current_node, dest_node, weight=weight_offen)
    
    def remove_node(self, node):
        if self._defensive_graph.has_node(node):
            self._defensive_graph.remove_node(node)
        
        if self._offensive_graph.has_node(node):
            self._offensive_graph.remove_node(node)
            
    def compute_path(self, from_node, to_node, defensive_mode):
        graph = self._select_graph(defensive_mode)
        
        return nx.astar_path(graph, from_node, to_node)

    def get_weight(self, path, defensive_mode):
        graph = self._select_graph(defensive_mode)

        return nx.path_weight(graph, path, 'weight')

    def _select_graph(self, defensive_mode):
        if defensive_mode:
            return self._defensive_graph
        
        return self._offensive_graph

