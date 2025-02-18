from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, lpSum

def solve_linear_programming(data):
    """
    data = {
        "objective": [3, 5],  # Coefficients of the objective function
        "constraints": [
            {"coefficients": [2, 1], "operator": "<=", "rhs": 8},
            {"coefficients": [1, 2], "operator": "<=", "rhs": 6}
        ],
        "bounds": [(0, None), (0, None)],  # Variable bounds
        "optimization_type": "max"  # "max" for maximization, "min" for minimization
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

    # Solve the model
    model.solve()

    return {
        "status": model.status,
        "objective_value": model.objective.value(),
        "variables": {var.name: var.value() for var in variables}
    }
