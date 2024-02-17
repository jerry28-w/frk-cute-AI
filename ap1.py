from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json


app = Flask(__name__, template_folder='templates')  # Specify the template folder
CORS(app, resources={r"/check_vulgarity": {"origins": "*"}})

# Enable CORS for all routes
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Function to check if a sentence contains vulgarity
def contains_vulgarity(sentence):
    # Set up parameters for the API call
    url = "https://8e36-2405-201-d00f-1023-7994-c9b0-7924-7db1.ngrok-free.app/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "system", "content": "Is the following sentence or paragraph inappropriate or contains vulgarity? Please mention the inappropriate content and also give its appropriate alternative"},
            {"role": "user", "content": f"'{sentence}'"}
        ]
    }
    
    # Make an API call to check for vulgarity
    response = requests.post(url, headers=headers, json=data)
    result = json.loads(response.text)
    
    # Analyze the content of the response for vulgarity indication
    if any(keyword in result["choices"][0]["message"]["content"].lower() for keyword in ["yes", "is inappropriate", "contains vulgarity", "contains multiple"]):
        return result["choices"][0]["message"]["content"].lower()
    elif any(keyword in result["choices"][0]["message"]["content"].lower() for keyword in ["no", "is not inappropriate or vulgar", "no inappropriate content present"]):
        return False

    
# Function to process input sentence and generate alternative if necessary
def process_sentence(input_sentence):
    # Check if input_sentence contains vulgarity
    return contains_vulgarity(input_sentence)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_vulgarity', methods=['POST'])
def check_vulgarity():
    user_input = request.json.get('sentence')
    result = process_sentence(user_input)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
