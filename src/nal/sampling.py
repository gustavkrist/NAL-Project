import networkx as nx
import random
import numpy as np
from collections import deque

def forest_fire(G: nx.Graph, sample_size : int = 100, p : float = 0.4, max_hops : int = 10, seed : int = None) -> nx.Graph:
    if seed:
        random.seed(seed)
        np.random.seed(seed)

    sample_nodes = set()
    visited_nodes = deque()
    all_nodes = set(G.nodes)
    
    while len(sample_nodes) < sample_size:
        remaining = list(all_nodes.difference(sample_nodes))
        if seed:
            remaining.sort()
        start_node = remaining[np.random.randint(0, len(remaining))]
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

            unvisited_neighbours = list(set(G.neighbors(cur_node)).difference(sample_nodes))
            if seed:
                unvisited_neighbours.sort()
            number_of_burned_neighbours = min(len(unvisited_neighbours), np.random.geometric(p))
            random.shuffle(unvisited_neighbours)
            burned_neighbours = unvisited_neighbours[:number_of_burned_neighbours]
            visited_nodes.extendleft(set(unvisited_neighbours).difference(set(burned_neighbours)))

            for n in burned_neighbours:
                if len(sample_nodes) >= sample_size:
                    break
                queue.extend([n])
        break
    return nx.Graph(nx.induced_subgraph(G, sample_nodes))
    