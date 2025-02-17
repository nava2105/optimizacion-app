import math


def solve_inventory_problem(data):
    """
    Calculates EOQ (Economic Order Quantity) based on:

    data = {
        "demand": 1000,  # Annual demand
        "ordering_cost": 50,  # Cost per order
        "holding_cost": 2  # Holding cost per unit per year
    }
    """

    demand = data["demand"]
    ordering_cost = data["ordering_cost"]
    holding_cost = data["holding_cost"]

    # Calculate EOQ
    eoq = math.sqrt((2 * demand * ordering_cost) / holding_cost)

    return {
        "status": "success",
        "eoq": round(eoq, 2),
        "annual_orders": round(demand / eoq, 2),
        "cycle_time": round(365 / (demand / eoq), 2)  # Days between orders
    }
