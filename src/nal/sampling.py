import networkx as nx
import random
import numpy as np
from collections import deque

def forest_fire(G: nx.Graph, sample_size : int = 100, p : float = 0.4, max_hops : int = 10) -> nx.Graph:
    sample_nodes = set()
    visited_nodes = deque()
    all_nodes = set(G.nodes)
    while len(sample_nodes) < sample_size:
        remaining = list(all_nodes.difference(sample_nodes))
        start_node = random.choice(remaining)
        sample_nodes.add(start_node)

        queue = deque([start_node])
        while len(sample_nodes) < sample_size:
            if len(queue) == 0:
                q = deque([visited_nodes.popleft() for x in range(min(max_hops, len(visited_nodes))) ])
                if len(queue) == 0:
                    print("not enough nodes")
                    break
            cur_node = queue.popleft()
            sample_nodes.add(cur_node)

            unvisited_neighbours = set(G.neighbors(cur_node)).difference(sample_nodes)
            number_of_burned_neighbours = min(len(unvisited_neighbours), np.random.geometric(p))
            burned_neighbours = random.sample(unvisited_neighbours, number_of_burned_neighbours)
            visited_nodes.extendleft(unvisited_neighbours.difference(set(burned_neighbours)))

            for n in burned_neighbours:
                if len(sample_nodes) >= sample_size:
                    break
                queue.extend([n])
        break
    return nx.Graph(nx.induced_subgraph(G, sample_nodes))
    