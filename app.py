from flask import Flask, jsonify, request

# Initialize the Flask app
app = Flask(__name__)

# Define a simple route to check if the app is working
@app.route('/')
def home():
    return "Hello, World!"

# A route to return some JSON data
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "This is a sample API response",
        "status": "success"
    }
    return jsonify(data)

# A route to handle POST requests
@app.route('/api/data', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()
        # Process the data here (e.g., store it or use it)
        response = {
            "message": "Data received successfully",
            "received_data": data
        }
        return jsonify(response), 201
    else:
        return jsonify({"error": "Request must be JSON"}), 400

# Error handling route for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

# Error handling route for internal server errors
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
