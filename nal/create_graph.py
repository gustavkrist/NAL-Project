import csv
import os
import pickle
from collections import defaultdict
from typing import Dict

import networkx as nx
from numpy import abs

from .load_config import load_config


def load_graph(
    save: bool = None, cache: bool = None, config_path: str = ""
) -> nx.classes.graph.Graph:
    config = load_config(config_path)
    data_location = config["data_location"]
    cache_location = config["cache_location"]
    save = save or config["save"]
    cache = cache or config["cache"]
    if cache:
        if os.path.exists(cache_location + "network.PKL"):
            with open(cache_location + "network.PKL", "rb") as f:
                return pickle.load(f)
    edgelist = project(
        on_file="rotten_tomatoes_movies.csv", data_location=data_location
    )
    G = nx.from_dict_of_dicts(edgelist)
    if save:
        with open(cache_location + "network.PKL", "wb+") as f:
            pickle.dump(G, f)
    return G


def project(
    primary_column: str = "rotten_tomatoes_link",
    on_column: str = "actors",
    ratings_column: str = "tomatometer_rating",
    on_file: str = "rotten_tomatoes_movies.csv",
    data_location: str = "data/extracted",
) -> Dict[str, Dict[str, Dict[str, int]]]:
    projection = defaultdict(list)
    ratings = dict()
    with open(data_location + on_file) as csv_file:
        rotten_tomatoes = csv.reader(csv_file, delimiter=",", quotechar='"')
        for i, line in enumerate(rotten_tomatoes):
            if not i:
                head = line
            else:
                lookup = dict(zip(head, line))
                ratings[lookup[primary_column]] = lookup[ratings_column]
                actors = lookup[on_column].strip().split(", ")
                for actor in actors:
                    if actor:
                        projection[actor].append(lookup[primary_column])
    edgelist: Dict[str, Dict[str, Dict[str, int]]] = defaultdict(dict)
    for values in projection.values():
        for i, movie1 in enumerate(values):
            for movie2 in values[i + 1 :]:
                if ratings[movie1] and ratings[movie2]:
                    edgelist[movie1][movie2] = {
                        "weight": abs(int(ratings[movie1]) - int(ratings[movie2]))
                    }
    return edgelist
