from typing import Generator
import networkx as nx


def connected_components(G: nx.Graph) -> Generator[set[str | int], None, None]: ...
