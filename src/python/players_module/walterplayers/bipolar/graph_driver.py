import networkx as nx


class GraphDriver:
    
    def __init__(self):
        self._defensive_graph = nx.Graph()
        self._offensive_graph = nx.Graph()

    