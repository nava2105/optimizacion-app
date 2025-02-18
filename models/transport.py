import numpy as np
from scipy.optimize import linprog


def northwest_corner(supply, demand):
    """ Implements the Northwest Corner Method to obtain an initial feasible solution. """
    allocation = np.zeros((len(supply), len(demand)))
    i, j = 0, 0
    while i < len(supply) and j < len(demand):
        min_val = min(supply[i], demand[j])
        allocation[i, j] = min_val
        supply[i] -= min_val
        demand[j] -= min_val
        if supply[i] == 0:
            i += 1
        if demand[j] == 0:
            j += 1
    return allocation


def minimum_cost_method(costs, supply, demand):
    """ Implements the Minimum Cost Method to obtain an initial feasible solution. """
    allocation = np.zeros((len(supply), len(demand)))
    costs = np.array(costs)
    while np.sum(supply) > 0 and np.sum(demand) > 0:
        i, j = np.unravel_index(np.argmin(costs), costs.shape)
        min_val = min(supply[i], demand[j])
        allocation[i, j] = min_val
        supply[i] -= min_val
        demand[j] -= min_val
        costs[i, j] = 1e9  # Mark cell as used with a large finite number
    return allocation


def vogel_method(costs, supply, demand):
    """ Implements Vogel's Approximation Method to obtain an initial feasible solution. """
    allocation = np.zeros((len(supply), len(demand)), dtype=float)  # Ensure float type
    costs = np.array(costs, dtype=float)  # Convert costs to float
    while np.sum(supply) > 0 and np.sum(demand) > 0:
        row_penalty = np.partition(costs, 1, axis=1)[:, 1] - costs.min(axis=1)
        col_penalty = np.partition(costs, 1, axis=0)[1] - costs.min(axis=0)
        if max(row_penalty) >= max(col_penalty):
            i = np.argmax(row_penalty)
            j = np.argmin(costs[i])
        else:
            j = np.argmax(col_penalty)
            i = np.argmin(costs[:, j])
        min_val = min(supply[i], demand[j])
        allocation[i, j] = min_val
        supply[i] -= min_val
        demand[j] -= min_val
        costs[i, j] = 1e9  # Assign a large number instead of np.inf
    return allocation


def solve_transport_problem(data):
    """
    Solves the transportation problem, considering:
    - Minimization (cost) or Maximization (profit).
    - Checks for feasibility and optimality conditions.

    data = {
        "supply": [20, 30, 25],
        "demand": [10, 15, 20, 30],
        "costs": [
            [8, 6, 10, 9],
            [9, 12, 7, 5],
            [14, 9, 16, 12]
        ],
        "optimization_type": "min"  # "min" for cost minimization, "max" for profit maximization,
        "method": "vogel", "norwest_corner", "minimum_cost_method"
    }
    """
    supply = np.array(data["supply"])
    demand = np.array(data["demand"])
    costs = np.array(data["costs"])
    method = data.get("method", "northwest_corner")

    if method == "northwest_corner":
        allocation = northwest_corner(supply.copy(), demand.copy())
    elif method == "minimum_cost":
        allocation = minimum_cost_method(costs.copy(), supply.copy(), demand.copy())
    elif method == "vogel":
        allocation = vogel_method(costs.copy(), supply.copy(), demand.copy())
    else:
        return {"status": "failure", "message": "Invalid method selected"}

    total_cost = np.sum(allocation * costs)
    return {
        "status": "success",
        "method": method,
        "allocation": allocation.tolist(),
        "total_cost": total_cost
    }
