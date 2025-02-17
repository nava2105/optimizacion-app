import numpy as np

def solve_knapsack_problem(data):
    """
    Solves the 0/1 Knapsack problem.

    data = {
        "capacity": 50,  # Maximum weight the knapsack can hold
        "items": [
            {"weight": 10, "value": 60},
            {"weight": 20, "value": 100},
            {"weight": 30, "value": 120}
        ]
    }
    """

    capacity = data["capacity"]
    items = data["items"]
    n = len(items)

    weights = [item["weight"] for item in items]
    values = [item["value"] for item in items]

    # Dynamic programming table
    dp = np.zeros((n + 1, capacity + 1))

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]

    # Find which items are included
    w = capacity
    selected_items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(items[i - 1])
            w -= weights[i - 1]

    return {
        "status": "success",
        "max_value": dp[n][capacity],
        "selected_items": selected_items
    }
