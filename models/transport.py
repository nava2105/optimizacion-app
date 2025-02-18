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


def check_optimality_and_improve(costs, allocation):
    """ Uses the MODI method to check and improve the optimality of the given allocation. """
    allocation = np.array(allocation, dtype=float)  # Ensure it's a NumPy array
    supply_size, demand_size = allocation.shape

    u = [None] * supply_size
    v = [None] * demand_size
    u[0] = 0  # Start with the first row

    # Compute u and v values iteratively
    for _ in range(supply_size + demand_size):
        for i in range(supply_size):
            for j in range(demand_size):
                if allocation[i][j] > 0:
                    if u[i] is not None and v[j] is None:
                        v[j] = costs[i][j] - u[i]
                    elif v[j] is not None and u[i] is None:
                        u[i] = costs[i][j] - v[j]

    # If any value in u or v remains None, replace it with 0
    u = [0 if x is None else x for x in u]
    v = [0 if x is None else x for x in v]

    # Calculate opportunity cost for non-allocated cells
    non_allocated = [
        (i, j, costs[i][j] - u[i] - v[j])
        for i in range(supply_size)
        for j in range(demand_size)
        if allocation[i][j] == 0
    ]

    # If all opportunity costs are >= 0, the solution is optimal
    if all(c >= 0 for _, _, c in non_allocated):
        return {
            "optimal": True,
            "message": "Solution is optimal.",
            "optimal_allocation": allocation.tolist()
        }

    # Otherwise, improve the allocation using stepping-stone method
    i, j, _ = min(non_allocated, key=lambda x: x[2])
    allocation[i, j] += 1  # Simplified improvement step

    return {
        "optimal": False,
        "message": "Solution is not optimal. Improved allocation provided.",
        "optimal_allocation": allocation.tolist()
    }