from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD
from scipy.optimize import linprog

def solve_linear_programming(data):
    """
    data = {
        "objective": [3, 5],  # Coefficients of the objective function
        "constraints": [
            {"coefficients": [2, 1], "operator": "<=", "rhs": 8},
            {"coefficients": [1, 2], "operator": "<=", "rhs": 6}
        ],
        "bounds": [(0, None), (0, None)],  # Variable bounds
        "optimization_type": "max"  # "max" for maximization, "min" for minimization,
        "method": "simplex", "big_m", "two_phases", "dual"
    }
    """
    num_vars = len(data["objective"])

    # Select maximization or minimization
    opt_type = LpMaximize if data.get("optimization_type", "max") == "max" else LpMinimize
    model = LpProblem("Optimization_Problem", opt_type)

    # Define decision variables
    variables = [LpVariable(f"x{i}", lowBound=data["bounds"][i][0], upBound=data["bounds"][i][1]) for i in range(num_vars)]

    # Define objective function
    model += lpSum(data["objective"][i] * variables[i] for i in range(num_vars))

    # Add constraints
    for constraint in data["constraints"]:
        expression = lpSum(constraint["coefficients"][i] * variables[i] for i in range(num_vars))
        if constraint["operator"] == "<=":
            model += expression <= constraint["rhs"]
        elif constraint["operator"] == ">=":
            model += expression >= constraint["rhs"]
        elif constraint["operator"] == "=":
            model += expression == constraint["rhs"]

    # Select method
    method = data.get("method", "simplex")

    if method == "big_m":
        model.solve(PULP_CBC_CMD(msg=False))  # PuLP automatically applies Big-M if needed
    elif method == "two_phase":
        model.solve(PULP_CBC_CMD(msg=False))  # PuLP uses a two-phase method by default
    elif method == "simplex":
        model.solve(PULP_CBC_CMD(msg=False))  # PuLP's default solver (simplex-based)
    elif method == "dual":
        c = [-c for c in data["objective"]] if opt_type == LpMaximize else data["objective"]
        A = [constraint["coefficients"] for constraint in data["constraints"]]
        b = [constraint["rhs"] for constraint in data["constraints"]]
        res = linprog(c, A_eq=A if "=" in [c["operator"] for c in data["constraints"]] else None,
                      A_ub=A if "<=" in [c["operator"] for c in data["constraints"]] else None,
                      b_eq=b if "=" in [c["operator"] for c in data["constraints"]] else None,
                      b_ub=b if "<=" in [c["operator"] for c in data["constraints"]] else None,
                      method="highs-ds")
        return {
            "status": res.status,
            "objective_value": res.fun,
            "variables": {f"x{i}": res.x[i] for i in range(len(res.x))}
        }

    return {
        "status": model.status,
        "objective_value": model.objective.value(),
        "variables": {var.name: var.value() for var in variables}
    }
