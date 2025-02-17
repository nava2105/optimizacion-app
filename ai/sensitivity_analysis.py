import numpy as np
from sklearn.linear_model import LinearRegression

def analyze_sensitivity(data):
    """
    Simula un análisis de sensibilidad variando restricciones y evaluando impacto en la solución óptima.
    """
    X = np.array(data["scenarios"])  # Variaciones en restricciones
    y = np.array(data["objective_values"])  # Cambios en la función objetivo

    model = LinearRegression()
    model.fit(X, y)

    sensitivity = model.coef_

    return {
        "sensitivity_coefficients": sensitivity.tolist(),
        "intercept": model.intercept_
    }
