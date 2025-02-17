from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from models.linear_programming import solve_linear_programming
from models.transport import solve_transport_problem
from models.network import solve_network_problem
from models.inventory import solve_inventory_problem
from models.dynamic_programming import solve_knapsack_problem
from ai.sensitivity_analysis import analyze_sensitivity

app = Flask(__name__)
api = Api(app)

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

api.add_resource(LinearProgrammingAPI, "/linear-programming")
api.add_resource(TransportAPI, "/transport")
api.add_resource(NetworkAPI, "/network")
api.add_resource(InventoryAPI, "/inventory")
api.add_resource(DynamicProgrammingAPI, "/dynamic-programming")
api.add_resource(SensitivityAnalysisAPI, "/sensitivity-analysis")

if __name__ == "__main__":
    app.run(debug=True)
