import csv
import os
import pickle
from collections import defaultdict

import networkx as nx

from .load_config import load_config


def load_graph(save=None, cache=None, config_path=""):
    config = load_config(config_path)
    data_location = config["data_location"]
    cache_location = config["cache_location"]
    save = config["save"] if save is None else save
    cache = config["cache"] if cache is None else cache
    if cache:
        if os.path.exists(cache_location + "network.PKL"):
            with open(cache_location + "network.PKL", "rb") as f:
                return pickle.load(f)
    edgelist = project(
        on_file="rotten_tomatoes_movies.csv", data_location=data_location
    )
    G = nx.Graph()
    G.add_edges_from(edgelist)
    if save:
        with open(cache_location + "network.PKL", "wb+") as f:
            pickle.dump(G, f)
    return G


def project(
    primary_column="rotten_tomatoes_link",
    on_column="actors",
    on_file="rotten_tomatoes_movies.csv",
    data_location="data/extracted",
):
    projection = defaultdict(list)
    with open(data_location + on_file) as csv_file:
        rotten_tomatoes = csv.reader(csv_file, delimiter=",", quotechar='"')
        for i, line in enumerate(rotten_tomatoes):
            if not i:
                head = line
            else:
                lookup = {k: v for k, v in zip(head, line)}
                actors = lookup[on_column].strip().split(", ")
                for actor in actors:
                    if actor:
                        projection[actor].append(lookup[primary_column])
    edgelist = []
    for values in projection.values():
        for i, movie1 in enumerate(values):
            for movie2 in values[i + 1 :]:
                edgelist.append((movie1, movie2))
    return edgelist
