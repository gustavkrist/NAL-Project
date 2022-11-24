from typing import Any

import networkx as nx

def from_dict_of_dicts(
    d: dict[str, dict[str, dict[str, int]]],
    create_using: Any = None,
    multigraph_input: Any = None,
) -> nx.Graph: ...
