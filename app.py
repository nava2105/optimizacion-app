from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource
from models.linear_programming import solve_linear_programming
from models.transport import solve_transport_problem
from models.network import solve_network_problem
from models.inventory import solve_inventory_problem
from models.dynamic_programming import solve_knapsack_problem
from ai.sensitivity_analysis import analyze_sensitivity, train_sensitivity_model

app = Flask(__name__)
api = Api(app)

# ------------------- API ROUTES -------------------
class LinearProgrammingAPI(Resource):
    def post(self):
        data = request.get_json()
        result = solve_linear_programming(data)
        return jsonify(result)

class TransportAPI(Resource):
    def post(self):
        data = request.get_json()
        result = solve_transport_problem(data)
        return jsonify(result)

class NetworkAPI(Resource):
    def post(self):
        data = request.get_json()
        result = solve_network_problem(data)
        return jsonify(result)

class InventoryAPI(Resource):
    def post(self):
        data = request.get_json()
        result = solve_inventory_problem(data)
        return jsonify(result)

class DynamicProgrammingAPI(Resource):
    def post(self):
        data = request.get_json()
        result = solve_knapsack_problem(data)
        return jsonify(result)

class SensitivityAnalysisAPI(Resource):
    def post(self):
        data = request.get_json()
        result = analyze_sensitivity(data)
        return jsonify(result)

class TrainSensitivityAPI(Resource):
    def post(self):
        data = request.get_json()
        train_sensitivity_model(data["scenarios"], data["objective_values"])
        return jsonify({"message": "Sensitivity model trained successfully."})

api.add_resource(LinearProgrammingAPI, "/api/linear-programming")
api.add_resource(TransportAPI, "/api/transport")
api.add_resource(NetworkAPI, "/api/network")
api.add_resource(InventoryAPI, "/api/inventory")
api.add_resource(DynamicProgrammingAPI, "/api/dynamic-programming")
api.add_resource(SensitivityAnalysisAPI, "/api/sensitivity-analysis")
api.add_resource(TrainSensitivityAPI, "/api/train-sensitivity")

# ------------------- FRONTEND ROUTES -------------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/linear-programming')
def linear_programming():
    return render_template("linear_programming.html")

@app.route('/transport')
def transport():
    return render_template("transport.html")

@app.route('/network')
def network():
    return render_template("network.html")

@app.route('/inventory')
def inventory():
    return render_template("inventory.html")

@app.route('/dynamic-programming')
def dynamic_programming():
    return render_template("dynamic_programming.html")

@app.route('/sensitivity-analysis')
def sensitivity_analysis():
    return render_template("sensitivity_analysis.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
