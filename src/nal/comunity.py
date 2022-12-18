from src.nal.create_graph import load_graph
from src.nal.analyze_communities import actor_significance
from src.nal.load_config import load_config
from networkx.algorithms.community import louvain_communities as alg
import networkx as nx
import pickle
import os


def discover_communities_and_their_most_significant_actors(resolution_param : float = 1.5):
    cache_location = './data/cache/'
    file_name = "communities.louvain." + str(resolution_param) + ".PKL"

    config = load_config()
    save = config["save"]
    cache = config["cache"]

    network = load_graph(config_path = './user/config.json')

    communities = []

    if cache and os.path.exists(cache_location + file_name):
                with open(cache_location + file_name, "rb") as f:
                    communities = pickle.load(f)
    else:
        communities = alg(network, resolution=resolution_param)

    if save:
        with open(cache_location + file_name, "wb+") as f:
            pickle.dump(communities, f)

    total_actor_count = actor_significance(list(network), config_path = './user/config.json')

    for i, c in enumerate(communities):
        l = len(list(c))
        if l < 20:
            continue
        com = actor_significance(list(c), config_path = './user/config.json')
        sig = [actor for actor, v in com.items() if v==max(com.values())][0]
        print("community {}'s most significant actor was {}, with {} occurences and representation of {}% and a reflection of {}%, size of community {}"
                .format(i, sig, com[sig], com[sig]/l*100, com[sig]/total_actor_count[sig]*100, l))
        H = nx.Graph(nx.induced_subgraph(network, c))
        edges = sorted(H.edges(data=True),key= lambda x: x[2]['weight'],reverse=True)
        max_weight = edges[0][2]['weight']
        min_weight = edges[-1][2]['weight']
        avg_weight = sum(map(lambda x: x[2]['weight'], edges)) / len(list(edges))
        print("community {}'s biggest rating difference {}, smallest rating difference {}, average rating difference {}".format(i, max_weight, min_weight, avg_weight))
        print("----------------------------------------------------------------------------------------------------------------------")
        

if __name__ == "__main__":
    discover_communities_and_their_most_significant_actors(2)