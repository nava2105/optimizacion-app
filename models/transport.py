import numpy as np
from scipy.optimize import linprog

def solve_transport_problem(data):
    """
    data = {
        "supply": [20, 30, 25],  # Supply at each source
        "demand": [10, 15, 20, 30],  # Demand at each destination
        "costs": [  # Cost matrix
            [8, 6, 10, 9],
            [9, 12, 7, 5],
            [14, 9, 16, 12]
        ],
        "optimization_type": "min"  # "min" for cost minimization, "max" for profit maximization
    }
    """

    supply = np.array(data["supply"])
    demand = np.array(data["demand"])
    costs = np.array(data["costs"])

    num_sources = len(supply)
    num_destinations = len(demand)

    # Objective function coefficients (flattened cost matrix)
    c = costs.flatten()
    if data.get("optimization_type", "min") == "max":
        c = -c  # Convert to maximization by negating the costs

    # Constraint matrix
    A_eq = np.zeros((num_sources + num_destinations, num_sources * num_destinations))
    b_eq = np.concatenate([supply, demand])

    for i in range(num_sources):
        A_eq[i, i * num_destinations:(i + 1) * num_destinations] = 1

    for j in range(num_destinations):
        A_eq[num_sources + j, j::num_destinations] = 1

    bounds = [(0, None) for _ in range(num_sources * num_destinations)]

    # Solve the optimization problem
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

    if result.success:
        transport_plan = result.x.reshape(num_sources, num_destinations).tolist()
        optimal_cost = -result.fun if data.get("optimization_type", "min") == "max" else result.fun
        return {"status": "success", "cost": optimal_cost, "transport_plan": transport_plan}
    else:
        return {"status": "failure", "message": "Failed to solve transportation problem"}
