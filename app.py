from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)

# Configure the Gemini model
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "You are a professional historian with years of experience. You will respond to the user's prompt in a concise way and if it is not about history remind the user to ask only about history and not answer his original prompt"},
        {"role": "model", "parts": "Hey ! What would you like to know?"},
    ]
)

# Function to check if a message is history-related (simple keyword-based filter)
def is_history_related(message):
    history_keywords = ['history', 'historical', 'ancient', 'war', 'empire', 'king', 'queen', 'battle', 'dynasty', 'civilization']
    return any(re.search(r'\b' + keyword + r'\b', message, re.IGNORECASE) for keyword in history_keywords)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    
    if user_message:
        # Check if the message is history-related
        if is_history_related(user_message):
            response = chat.send_message(user_message)
            return jsonify({'reply': response.text})
        else:
            return jsonify({'reply': 'Please ask questions related to history.'})
    
    return jsonify({'reply': 'Sorry, I did not understand that.'}), 400

if __name__ == '__main__':
    app.run(debug=True)