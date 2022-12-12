from __future__ import annotations

import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

import src.nal.sampling as sampling

def invert_weights(G : nx.Graph) -> nx.Graph:
    # find maximal weight
    max_weight = max([edge[2]['weight'] for edge in G.edges(data=True) ])

    # new edge weight is maximal weight - current weight -> sorted edges by weight will be 
    for edge in G.edges(data=True):
        edge[2]['weight'] = max_weight - edge[2]['weight']

    return G

def _check_or_create_path(path: str) -> None:
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))


def plot_degree_distribution(G: nx.Graph, filename: str) -> None:
    _check_or_create_path(filename)
    ext = "" if filename.removesuffix(".png") == filename else ".png"
    degree_sequence = [d for _, d in G.degree()]
    unique, counts = np.unique(degree_sequence, return_counts=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Degree distribution of graph")
    ax.set_xlabel("Degree")
    ax.set_ylabel("Count")
    ax.plot(unique, counts)
    plt.savefig(f"{filename}{ext}", dpi=400, bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Degree distribution of graph (log-log)")
    ax.set_xlabel("Degree (log)")
    ax.set_xscale("log")
    ax.set_ylabel("Count (log)")
    ax.set_yscale("log")
    ax.plot(unique, counts)
    plt.savefig(f"{filename}-log{ext}", dpi=400, bbox_inches="tight")

    cumulative = []
    for degree in unique:
        mask = np.where(unique >= degree)
        cumulative.append(counts[mask].sum() / counts.sum())

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Cumulative degree distribution of graph")
    ax.set_xlabel("Degree")
    ax.set_ylabel("Count")
    ax.plot(unique, cumulative)
    plt.savefig(f"{filename}-cumulative{ext}", dpi=400, bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Cumulative degree distribution of graph (log-log)")
    ax.set_xlabel("Degree (log)")
    ax.set_xscale("log")
    ax.set_ylabel("Count (log)")
    ax.set_yscale("log")
    ax.plot(unique, cumulative)
    plt.savefig(f"{filename}-cumulative-log{ext}", dpi=400, bbox_inches="tight")


def basic_statistics(
    G: nx.Graph, format: str = "latex", filename: str | None = None, average_repetitions: int = 100
) -> None:
    # TODO: Investigate whether these are too slow to feasibly run
    # they are too slow, so the samplig method

    avg_clustering_coef = 0
    avg_clustering_coef_weighted = 0
    for x in range(average_repetitions):
        H = sampling.forest_fire(G)
        avg_clustering_coef += nx.average_clustering(H)

        # # FIXME: Higher weights = higher clustering, so need inverse differential of ratings
        # # Fixed with inverting edges
        H = invert_weights(H)
        avg_clustering_coef_weighted += nx.average_clustering(H, weight="weight")


    avg_clustering_coef /= average_repetitions
    avg_clustering_coef_weighted /= average_repetitions


    density = nx.density(G)
    avg_eig_centrality = np.mean(list(nx.eigenvector_centrality(G).values()))

    statistics = [
        "Average Clustering Coefficient",
        "Average (Weighted) Clustering Coefficient",
        "Average Eigenvalue Centrality",
        "Density",
    ]
    values = [
        avg_clustering_coef,
        avg_clustering_coef_weighted,
        avg_eig_centrality,
        density,
    ]

    df = pd.DataFrame({"Statistic": statistics, "Value": values})

    if format == "latex":
        output = df.to_latex(index=False)
    elif format == "markdown":
        output = df.to_markdown(index=False)
    elif format == "csv":
        output = df.to_csv(index=False)
    else:
        raise ValueError(
            f"Value of argument {format=} is invalid. "
            "Valid options are: latex, markdown and csv"
        )

    if filename is not None:
        _check_or_create_path(filename)
        with open(filename, "w") as f:
            f.write(output)
    else:
        print(output)
