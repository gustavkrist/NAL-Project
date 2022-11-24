import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def plot_degree_distribution(G: nx.Graph, filename: str) -> None:
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    degree_sequence = sorted((d for _, d in G.degree()), reverse=True)
    unique, counts = np.unique(degree_sequence, return_counts=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Degree distribution of graph")
    ax.set_xlabel("Degree")
    ax.set_ylabel("Count")
    ax.plot(unique, counts)
    plt.savefig(f'{filename}.png', dpi=400, bbox_inches='tight')

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Degree distribution of graph (log-log)")
    ax.set_xlabel("Degree (log)")
    ax.set_xscale("log")
    ax.set_ylabel("Count (log)")
    ax.set_yscale("log")
    ax.plot(unique, counts)
    plt.savefig(f'{filename}-log.png', dpi=400, bbox_inches='tight')
