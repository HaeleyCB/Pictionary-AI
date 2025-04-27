# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template_string
from flask_ngrok import run_with_ngrok
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import random
import io
import os

# Initialize the Flask app
app = Flask(__name__)

# Use ngrok to expose the Flask app to the internet
run_with_ngrok(app)  # This makes your app public

# Load the model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# List of fun prompts
prompts = [
    "a flying elephant", "a dinosaur at the beach", "a cat riding a skateboard",
    "a monster eating spaghetti", "a robot watering flowers", "a unicorn in space"
]

# HTML Template for rendering the game UI
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pictionary AI</title>
    <style>
        body { font-family: 'Comic Sans MS', cursive, sans-serif; background: #ffe; padding: 20px; text-align: center; }
        h1 { color: #ff6600; }
        button, input { margin: 10px; font-size: 1.2em; }
        #timer { font-size: 2em; color: red; }
    </style>
    <script>
        let timer;
        function startTimer() {
            let countdown = 60;
            document.getElementById('timer').innerText = countdown + ' seconds left!';
            timer = setInterval(function() {
                countdown--;
                document.getElementById('timer').innerText = countdown + ' seconds left!';
                if (countdown <= 0) {
                    clearInterval(timer);
                    alert("Time's up! Now upload your image.");
                }
            }, 1000);
        }
    </script>
</head>
<body>
    <h1>🎨 Pictionary AI 🎉</h1>
    <p><strong>Instructions:</strong></p>
    <p>1. Click 'Start' to get your drawing prompt.<br>
       2. Open the Procreate app.<br>
       3. Draw your image and take a screenshot/photo within 1 minute.<br>
       4. Click 'Choose File' and upload your drawing.<br>
       5. See if AI can guess what you drew!</p>

    {% if prompt %}
        <h2>Your Drawing Prompt: <em>{{ prompt }}</em></h2>
        <div id="timer"></div>
        <script>startTimer();</script>
    {% endif %}

    <form method="POST" enctype="multipart/form-data">
        <button name="start" type="submit">🎲 Start</button><br>
        <input type="file" name="image"><br>
        <button type="submit">📤 Upload</button>
    </form>

    {% if caption %}
        <h2>AI's Guess: 🤖 "{{ caption }}"</h2>
        <form method="POST">
            <button name="play_again" type="submit">🔁 Play Again</button>
        </form>
    {% endif %}
</body>
</html>
"""

# Route for the main page of the game
@app.route("/", methods=["GET", "POST"])
def index():
    prompt = caption = None
    if request.method == "POST":
        if 'start' in request.form:
            prompt = random.choice(prompts)
        elif 'image' in request.files:
            image_file = request.files['image']
            if image_file:
                # Process the uploaded image
                image = Image.open(io.BytesIO(image_file.read())).convert("RGB")
                inputs = processor(images=image, return_tensors="pt")
                out = model.generate(**inputs)
                caption = processor.decode(out[0], skip_special_tokens=True)
        elif 'play_again' in request.form:
            prompt = random.choice(prompts)

    return render_template_string(html_template, prompt=prompt, caption=caption)

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
    # Running the Flask app on 0.0.0.0 ensures it listens on all available network interfaces
    app.run(debug=True, host='0.0.0.0', port=5000)
