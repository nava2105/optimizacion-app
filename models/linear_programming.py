from pulp import LpMaximize, LpProblem, LpVariable, lpSum


def solve_linear_programming(data):
    """
    data = {
        "objective": [3, 5],  # Coeficientes de la función objetivo
        "constraints": [
            {"coefficients": [2, 1], "operator": "<=", "rhs": 8},
            {"coefficients": [1, 2], "operator": "<=", "rhs": 6}
        ],
        "bounds": [(0, None), (0, None)]  # Límites de las variables
    }
    """
    num_vars = len(data["objective"])

    # Definir el problema de maximización
    model = LpProblem("Maximization", LpMaximize)

    # Definir variables de decisión
    variables = [LpVariable(f"x{i}", lowBound=data["bounds"][i][0], upBound=data["bounds"][i][1]) for i in
                 range(num_vars)]

    # Definir función objetivo
    model += lpSum(data["objective"][i] * variables[i] for i in range(num_vars))

    # Agregar restricciones
    for constraint in data["constraints"]:
        expression = lpSum(constraint["coefficients"][i] * variables[i] for i in range(num_vars))
        if constraint["operator"] == "<=":
            model += expression <= constraint["rhs"]
        elif constraint["operator"] == ">=":
            model += expression >= constraint["rhs"]
        elif constraint["operator"] == "=":
            model += expression == constraint["rhs"]

    # Resolver el modelo
    model.solve()

    # Extraer resultados
    result = {
        "status": model.status,
        "objective_value": model.objective.value(),
        "variables": {var.name: var.value() for var in variables}
    }

    return result
