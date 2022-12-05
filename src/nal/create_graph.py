from __future__ import annotations

import csv
import os
import pickle
from collections import defaultdict
from typing import Dict

import networkx as nx
from numpy import abs, argmax

from .load_config import load_config


EdgeList = Dict[str, Dict[str, Dict[str, int]]]


def load_graph(
    save: bool | None = None, cache: bool | None = None, config_path: str = ""
) -> nx.Graph:
    config = load_config(config_path)
    data_location = config["data_location"]
    cache_location = config["cache_location"]
    save = save if save is not None else config["save"]
    cache = cache if cache is not None else config["cache"]
    if cache:
        if os.path.exists(cache_location + "network.PKL"):
            with open(cache_location + "network.PKL", "rb") as f:
                G: nx.Graph = pickle.load(f)
                return G
    edgelist = project(
        on_file="rotten_tomatoes_movies.csv", data_location=data_location
    )
    G = nx.from_dict_of_dicts(edgelist)
    if save:
        with open(cache_location + "network.PKL", "wb+") as f:
            pickle.dump(G, f)
    return extract_gcc(G)


def project(
    primary_column: str = "rotten_tomatoes_link",
    on_column: str = "actors",
    ratings_column: str = "tomatometer_rating",
    on_file: str = "rotten_tomatoes_movies.csv",
    data_location: str = "data/extracted",
) -> EdgeList:
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
    edgelist: EdgeList = defaultdict(dict)
    for values in projection.values():
        for i, movie1 in enumerate(values):
            for movie2 in values[i + 1 :]:
                if ratings[movie1] and ratings[movie2]:
                    edgelist[movie1][movie2] = {
                        "weight": abs(int(ratings[movie1]) - int(ratings[movie2]))
                    }
    return edgelist


def extract_gcc(G: nx.Graph) -> nx.Graph:
    ccs = list(nx.connected_components(G))
    biggest_cc = argmax(list(map(len, ccs)))
    gcc = ccs[biggest_cc]
    return G.subgraph(gcc)
