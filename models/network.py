import networkx as nx

def solve_network_problem(data):
    """
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

    # Agregar nodos y aristas con capacidad
    for edge in data["edges"]:
        G.add_edge(edge["from"], edge["to"], capacity=edge["capacity"])

    # Resolver flujo máximo
    flow_value, flow_dict = nx.maximum_flow(G, data["source"], data["sink"])

    return {
        "status": "success",
        "max_flow": flow_value,
        "flow_distribution": flow_dict
    }
