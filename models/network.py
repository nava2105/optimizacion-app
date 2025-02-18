import networkx as nx

def solve_network_problem(data):
    """
    Processes the network graph to compute:
    - Maximum Flow
    - Shortest Path (Dijkstra)
    - Longest Path (DAG only)
    - Minimum Spanning Tree (MST)

    data = {
        "edges": [
            {"from": "A", "to": "B", "capacity": 10},
            {"from": "A", "to": "C", "capacity": 15},
            {"from": "B", "to": "D", "capacity": 10},
            {"from": "C", "to": "D", "capacity": 5},
            {"from": "C", "to": "E", "capacity": 10},
            {"from": "D", "to": "E", "capacity": 10}
        ],
        "source": "A",
        "sink": "E"
    }
    """

    G = nx.DiGraph()

    # Add edges with weights
    for edge in data["edges"]:
        G.add_edge(edge["from"], edge["to"], capacity=edge["capacity"], weight=1 / (edge["capacity"] + 0.01))

    # Compute Maximum Flow
    flow_value, flow_dict = nx.maximum_flow(G, data["source"], data["sink"])

    # Compute Shortest Path (Dijkstra)
    try:
        shortest_path = nx.shortest_path(G, source=data["source"], target=data["sink"], weight="weight")
        shortest_path_length = nx.shortest_path_length(G, source=data["source"], target=data["sink"], weight="weight")
    except nx.NetworkXNoPath:
        shortest_path, shortest_path_length = None, float('inf')

    # Compute Longest Path (Only for DAGs)
    longest_path, longest_path_length = None, None
    if nx.is_directed_acyclic_graph(G):
        longest_path = nx.dag_longest_path(G)
        longest_path_length = len(longest_path) - 1

    # Compute Minimum Spanning Tree (MST) - Convert to undirected
    MST = nx.minimum_spanning_tree(G.to_undirected(), weight="capacity")
    mst_edges = [{"from": u, "to": v, "capacity": G[u][v]["capacity"]} for u, v in MST.edges()]

    return {
        "status": "success",
        "max_flow": flow_value,
        "flow_distribution": flow_dict,
        "shortest_path": shortest_path,
        "shortest_path_length": shortest_path_length,
        "longest_path": longest_path if longest_path else "Graph is not a DAG",
        "longest_path_length": longest_path_length if longest_path else "N/A",
        "minimum_spanning_tree": mst_edges
    }
