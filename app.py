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

# A route to render the homepage with HTML directly in the app.py
@app.route('/homepage')
def homepage():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Home Page</title>
        </head>
        <body>
            <h1>Welcome to the Homepage!</h1>
            <p>This is the homepage of your Flask app.</p>
        </body>
        </html>
    '''

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
    app.run(debug=True, host='0.0.0.0', port=5000)

    import os
from flask import Flask

# Create a Flask instance
app = Flask(__name__)

# Define a simple route for the homepage
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Run the app, using the PORT environment variable or default to 5000
if __name__ == '__main__':
    # Get the port from the environment variable (if set), default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app on all available network interfaces (0.0.0.0)
    # and on the specified port
    app.run(host='0.0.0.0', port=port)

