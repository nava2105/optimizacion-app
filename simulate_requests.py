import requests
import random
import time

# API Endpoints
API_TRAIN = "http://localhost:5000/api/train-sensitivity"
API_ANALYZE = "http://localhost:5000/api/sensitivity-analysis"

# Function to generate random training data
def generate_random_data():
    num_scenarios = random.randint(3, 6)  # Number of scenarios per request
    scenarios = [[random.randint(1, 20) for _ in range(3)] for _ in range(num_scenarios)]
    objective_values = [sum(scenario) + random.randint(-5, 5) for scenario in scenarios]
    return {"scenarios": scenarios, "objective_values": objective_values}

# Send multiple requests
num_requests = 50  # Change this to any number of requests you want
for i in range(num_requests):
    data = generate_random_data()

    # Train the model
    response = requests.post(API_TRAIN, json=data)
    print(f"Request {i+1}/{num_requests} - Training Response: {response.json()}")

    # Analyze sensitivity
    response = requests.post(API_ANALYZE, json=data)
    print(f"Request {i+1}/{num_requests} - Analysis Response: {response.json()}")

    time.sleep(1)  # Add delay to simulate real API usage
