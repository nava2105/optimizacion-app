import numpy as np
from scipy.optimize import linprog

def solve_transport_problem(data):
    """
    data = {
        "supply": [20, 30, 25],  # Oferta de cada origen
        "demand": [10, 15, 20, 30],  # Demanda de cada destino
        "costs": [  # Matriz de costos de transporte
            [8, 6, 10, 9],
            [9, 12, 7, 5],
            [14, 9, 16, 12]
        ]
    }
    """

    supply = np.array(data["supply"])
    demand = np.array(data["demand"])
    costs = np.array(data["costs"])

    num_sources = len(supply)
    num_destinations = len(demand)

    # Variables de decisión: minimizamos el costo de transporte
    c = costs.flatten()

    # Restricciones de oferta
    A_eq = np.zeros((num_sources + num_destinations, num_sources * num_destinations))
    b_eq = np.concatenate([supply, demand])

    # Restricciones de oferta (cada fila representa una fuente)
    for i in range(num_sources):
        A_eq[i, i * num_destinations:(i + 1) * num_destinations] = 1

    # Restricciones de demanda (cada columna representa un destino)
    for j in range(num_destinations):
        A_eq[num_sources + j, j::num_destinations] = 1

    # Restricción de no-negatividad
    bounds = [(0, None) for _ in range(num_sources * num_destinations)]

    # Resolver el problema
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

    if result.success:
        transport_plan = result.x.reshape(num_sources, num_destinations).tolist()
        return {"status": "success", "cost": result.fun, "transport_plan": transport_plan}
    else:
        return {"status": "failure", "message": "No se pudo resolver el problema de transporte"}
