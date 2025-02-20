# Optimization Algorithms Web Application

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![PuLP](https://img.shields.io/badge/pulp-optimization-orange)
![NetworkX](https://img.shields.io/badge/networkx-graph%20theory-red)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fnava2105%2Foptimizacion-app.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fnava2105%2Foptimizacion-app?ref=badge_shield)

---

## **Table of Contents**
1. [General Info](#general-info)
2. [Features](#features)
3. [Technologies](#technologies)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [API Usage Examples](#api-usage-examples)
8. [Front-End Usage Examples](#front-end-usage-examples)

---

## **General Info**
This project is a **web-based application** that solves various **optimization problems**, including:
- **Linear Programming** (Simplex Method)
- **Network Optimization** (Max-Flow, Shortest Path, MST)
- **Knapsack Problem** (Dynamic Programming)
- **Economic Order Quantity (EOQ) Model**
- **Transportation Problem**
- **Sensitivity Analysis**

The application is built using **Flask** for the backend, and it provides both a **REST API** and a **user-friendly web interface**.

---

## **Features**
- **Solve multiple optimization problems**  
- **User-friendly web UI**  
- **API endpoints for automation**  
- **Visual representation of results**  

---

## **Technologies**
- **Backend**: Flask (Python)
- **Optimization Libraries**:
  - **PuLP** (Linear Programming)
  - **NetworkX** (Graph Optimization)
  - **NumPy** (Matrix Computations)
  - **SciPy** (Transport Problem)
- **Frontend**: HTML, JavaScript, Chart.js

---

## **Installation**

### Via Github

#### - **Prerequisites**
- **Python 3.9**
- **pip** installed

#### - **Steps**
1. Clone the repository:
    ```bash
    git clone https://github.com/nava2105/optimizacion-app.git
    cd optimization-app
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    python app.py
    ```

### Via Dockerhub

#### - **Prerequisites**
- **Docker running**

#### - **Steps**
1. Clone the repository:
    ```bash
    docker pull na4va4/optimization-app
    ```
2. Run the application:
    ```bash
    docker run -p 5000:5000 na4va4/optimization-app
    ```
   
---

## **Usage**

* Web UI: Open http://localhost:5000/
* API Access: Use endpoints to solve problems programmatically.

---

## **API Endpoints**

| **Problem Type**              | **Endpoint**               | **Method** |
|-------------------------------|----------------------------|------------|
| Linear Programming            | /api/linear-programming	   | POST       |
| Knapsack Problem              | /api/dynamic-programming	  | POST       |
| Economic Order Quantity (EOQ) | 	/api/inventory            | 	POST      |
| Network Optimization	         | /api/network	              | POST       |              
| Transportation Problem	       | /api/transport	            | POST       |            
| Sensitivity Analysis	         | /api/sensitivity-analysis	 | POST       |

---

## **API Usage Examples**

### **Linear Programming**
**Request:**
```bash
curl -X POST http://localhost:5000/api/linear-programming -H "Content-Type: application/json" -d '{
    "objective": [3, 5],
    "constraints": [
        {"coefficients": [2, 1], "operator": "<=", "rhs": 8},
        {"coefficients": [1, 2], "operator": "<=", "rhs": 6}
    ],
    "bounds": [[0, null], [0, null]],
    "optimization_type": "max"
}'
```
**Response:**
```json
{
    "status": 1,
    "objective_value": 18.0,
    "variables": {"x0": 2.0, "x1": 3.0}
}
```

### **Transportation Problem**
**Request:**
```bash
curl -X POST http://localhost:5000/api/transport -H "Content-Type: application/json" -d '{
    "supply": [20, 30, 25],
    "demand": [10, 15, 20, 30],
    "costs": [
        [8, 6, 10, 9],
        [9, 12, 7, 5],
        [14, 9, 16, 12]
    ],
    "optimization_type": "min"
}'
```
**Response:**
```json
{
    "status": "success",
    "cost": 345.0,
    "transport_plan": [[10, 10, 0, 0], [0, 5, 20, 5], [0, 0, 0, 25]],
    "feasibility": "Feasible",
    "unused_supply": [0, 0, 0],
    "unmet_demand": [0, 0, 0, 0]
}
```

### **Network Optimization**
**Request:**
```bash
curl -X POST http://localhost:5000/api/network -H "Content-Type: application/json" -d '{
    "edges": [
        {"from": "A", "to": "B", "capacity": 10},
        {"from": "A", "to": "C", "capacity": 15},
        {"from": "B", "to": "D", "capacity": 10},
        {"from": "C", "to": "D", "capacity": 5},
        {"from": "C", "to": "E", "capacity": 10},
        {"from": "D", "to": "E", "capacity": 10}
    ],
    "source": "A",
    "sink": "E"
}'
```
**Response:**
```json
{
    "status": "success",
    "max_flow": 15,
    "flow_distribution": {"A": {"B": 10, "C": 5}, "B": {"D": 10}, "C": {"D": 5, "E": 0}, "D": {"E": 10}},
    "shortest_path": ["A", "C", "D", "E"],
    "shortest_path_length": 2.98,
    "longest_path": "Graph is not a DAG",
    "minimum_spanning_tree": [{"from": "A", "to": "B", "capacity": 10}, {"from": "B", "to": "D", "capacity": 10}, {"from": "D", "to": "E", "capacity": 10}]
}
```

### **Inventory Management (EOQ)**
**Request:**
```bash
curl -X POST http://localhost:5000/api/inventory -H "Content-Type: application/json" -d '{
    "demand": 1000,
    "ordering_cost": 50,
    "holding_cost": 2
}'
```
**Response:**
```json
{
    "status": "success",
    "eoq": 158.11,
    "annual_orders": 6.33,
    "cycle_time": 57.71
}
```

### **Knapsack Problem (0/1)**
**Request:**
```bash
curl -X POST http://localhost:5000/api/dynamic-programming -H "Content-Type: application/json" -d '{
    "capacity": 50,
    "items": [
        {"weight": 10, "value": 60},
        {"weight": 20, "value": 100},
        {"weight": 30, "value": 120}
    ]
}'
```
**Response:**
```json
{
    "status": "success",
    "max_value": 220,
    "selected_items": [
        {"weight": 20, "value": 100},
        {"weight": 30, "value": 120}
    ]
}
```

### **Sensitivity Analysis**
**Request:**
```bash
curl -X POST http://localhost:5000/api/sensitivity-analysis -H "Content-Type: application/json" -d '{
    "scenarios": [[10, 5, 3], [7, 9, 2]],
    "objective_values": [18, 15]
}'
```
**Response:**
```json
{
    "sensitivity_coefficients": [17.8, 14.9],
    "model_updated": true
}
```

---

## **Front-End Usage Examples**

### **Linear Programming**
**Steps:**
1. Navigate to the **Linear Programming** page from the menu.
2. Enter the objective function coefficients (comma-separated).
3. Enter constraints as rows (`coefficients, operator, rhs`).
4. Select `Maximization` or `Minimization`.
5. Click **Solve** to compute the optimal solution.

**Results Displayed:**
- Optimal objective function value.
- Decision variable values.
- Graphical representation using a bar chart.


### **Transportation Problem**
**Steps:**
1. Go to the **Transport Optimization** page.
2. Enter supply and demand values as comma-separated numbers.
3. Input the cost matrix with one row per line.
4. Choose between **Minimization (Cost)** or **Maximization (Profit)**.
5. Click **Solve**.

**Results Displayed:**
- Feasibility check.
- Total transport cost or profit.
- Transport plan in table format.
- Unused supply and unmet demand.
- Cost/profit graph.

### **Network Optimization**
**Steps:**
1. Navigate to the **Network Analysis** page.
2. Enter edges (`from,to,capacity`) one per line.
3. Set the **Source** and **Sink** nodes.
4. Click **Solve**.

**Results Displayed:**
- Maximum flow with distribution table.
- Shortest and longest paths.
- Minimum spanning tree.
- Flow visualization graph.

### **Inventory Management (EOQ)**
**Steps:**
1. Open the **Inventory Optimization** page.
2. Input **Annual Demand**, **Ordering Cost**, and **Holding Cost per Unit**.
3. Click **Solve**.

**Results Displayed:**
- Economic Order Quantity (EOQ).
- Number of orders per year.
- Days between orders.

### **Knapsack Problem (0/1)**
**Steps:**
1. Navigate to the **Dynamic Programming** page.
2. Set the knapsack **Capacity**.
3. Enter items as `weight,value` pairs, one per line.
4. Click **Solve**.

**Results Displayed:**
- Maximum achievable value.
- Selected items in table format.
- Graph representation of selected items.

### **Sensitivity Analysis**
**Steps:**
1. Go to the **Sensitivity Analysis** page.
2. Enter scenarios as comma-separated numbers per line.
3. Provide objective function values as a comma-separated list.
4. Click **Analyze**.

**Results Displayed:**
- Sensitivity coefficients per scenario.
- Updated model feedback.


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fnava2105%2Foptimizacion-app.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fnava2105%2Foptimizacion-app?ref=badge_large)