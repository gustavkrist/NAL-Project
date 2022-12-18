# type: ignore
from __future__ import annotations

import os
from collections import Counter

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import powerlaw as pl
from scipy.stats import linregress

import nal.sampling as sampling


def invert_weights(G: nx.Graph) -> nx.Graph:
    # find maximal weight
    max_weight = max([edge[2]["weight"] for edge in G.edges(data=True)])

    # new edge weight is maximal weight - current weight -> sorted edges by weight will be
    for edge in G.edges(data=True):
        edge[2]["weight"] = max_weight - edge[2]["weight"]

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
    ax.set_xlabel("k")
    ax.set_ylabel("Count")
    ax.plot(unique, counts)
    plt.savefig(f"{filename}{ext}", dpi=400, bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Degree distribution of graph (log-log)")
    ax.set_xlabel("k")
    ax.set_xscale("log")
    ax.set_ylabel("Count (log)")
    ax.set_yscale("log")
    ax.plot(unique, counts)
    plt.savefig(f"{filename}-log{ext}", dpi=400, bbox_inches="tight")

    cumulative = []
    for degree in unique:
        mask = np.where(unique >= degree)
        cumulative.append(counts[mask].sum() / counts.sum())

    _, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Cumulative degree distribution of graph (log-log)")
    ax.set_xlabel("k")
    ax.set_xscale("log")
    ax.set_ylabel("P(degree > k)")
    ax.set_yscale("log")
    ax.plot(unique, cumulative)
    plt.savefig(f"{filename}-cumulative-log{ext}", dpi=400, bbox_inches="tight")

    dd = Counter(dict(G.degree).values())
    dd = pd.DataFrame(list(dd.items()), columns = ("k", "count")).sort_values(by = "k")
    ccdf = dd.sort_values(by = "k", ascending = False)
    ccdf["cumsum"] = ccdf["count"].cumsum()
    ccdf["ccdf"] = ccdf["cumsum"] / ccdf["count"].sum()
    ccdf = ccdf[["k", "ccdf"]].sort_values(by = "k")
    # We take the logarithm in base 10 of both degree and CCDF. Then we simply do a linear regression. The slope is
    # the exponent. The intercept needs to be the power of 10, to undo the logarithm operation. Look at that
    # r-squared!
    logcdf = np.log10(ccdf[["k", "ccdf"]])
    slope, log10intercept, r_value, p_value, _ = linregress(logcdf["k"], logcdf["ccdf"])
    print("CCDF Fit: %1.4f x ^ %1.4f (R2 = %1.4f, p = %1.4f)" % (10 ** log10intercept, slope, r_value ** 2, p_value))
    # With the powerlaw package, fitting the CCDf is simple. It will store results in the .power_law property. To
    # get the actual k_min, we need to find the degree value corresponding to the probability in .power_law.xmin:
    # pandas makes it easy. This is definitely a shifted power law. (Kappa contains the intercept information)
    results = pl.Fit(ccdf["ccdf"])
    k_min = ccdf[ccdf["ccdf"] == results.power_law.xmin]["k"]
    print("Powerlaw CCDF Fit: %1.4f x ^ -%1.4f (k_min = %d)" % (10 ** results.power_law.Kappa, results.power_law.alpha, k_min))
    # Let's plot the best fit.
    ccdf["fit"] = (10 ** results.power_law.Kappa) * (ccdf["k"] ** -results.power_law.alpha)
    ax = plt.gca()
    ccdf.plot(kind = "line", x = "k", y = "ccdf", color = "#e41a1c", loglog = True, ax = ax)
    ccdf.plot(kind = "line", x = "k", y = "fit", color = "#377eb8", loglog = True, ax = ax)
    plt.savefig(f"{filename}-cumulative-log-powerlaw{ext}", dpi=400, bbox_inches="tight")


def basic_statistics(
    G: nx.Graph,
    format: str = "latex",
    filename: str | None = None,
    average_repetitions: int = 100,
) -> None:
    avg_clustering_coef = 0.0
    avg_clustering_coef_weighted = 0.0
    avg_betweenness_cent = 0.0
    for x in range(average_repetitions):
        H = sampling.forest_fire(G)
        avg_clustering_coef += nx.average_clustering(H)
        avg_betweenness_cent += np.mean(list(nx.betweenness_centrality(H).values()))

        H = invert_weights(H)
        avg_clustering_coef_weighted += nx.average_clustering(H, weight="weight")

    avg_clustering_coef /= average_repetitions
    avg_clustering_coef_weighted /= average_repetitions
    avg_betweenness_cent /= average_repetitions

    density = nx.density(G)

    statistics = [
        "Number of Nodes",
        "Number of Edges",
        "Average Degree",
        "Density",
        "Average Clustering Coefficient",
        "Average (Weighted) Clustering Coefficient",
        "Average Betweenness Centrality",
    ]
    values = [
        len(G.nodes),
        len(G.edges),
        np.mean(tuple(d for _, d in G.degree)),
        avg_clustering_coef,
        avg_clustering_coef_weighted,
        avg_betweenness_cent,
        density,
    ]

    df = pd.DataFrame({"Statistic": statistics, "Value": values})

    if format == "latex":
        formatters = {"Value": lambda x: str(int(x)) if x.is_integer() else f"{x:.4f}"}
        output = rf"""
        \documentclass{{paper}}
        \usepackage{{booktabs}}
        \usepackage[table]{{xcolor}}
        \begin{{document}}
        \rowcolors{{2}}{{gray!25}}{{white}}
        {df.to_latex(index=False, formatters=formatters)}
        \end{{document}}"""
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
