###
# NE FONCTIONNE PAS
###
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from google.oauth2 import service_account

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set up Google authentication using service account credentials
credentials = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
)

# Configure the Generative AI API with OAuth2 credentials
genai.configure(credentials=credentials)

# Model name for fine-tuning
base_model = "models/gemini-1.5-flash-001-tuning"

# Training data for fine-tuning the model to a historian persona
training_data = [
    {"text_input": "Tell me about the Renaissance.", 
     "output": "The Renaissance was a fervent period of European cultural, artistic, political, and economic 'rebirth' following the Middle Ages, typically considered to have occurred from the 14th to the 17th century."},
    
    {"text_input": "Who was Julius Caesar?", 
     "output": "Gaius Julius Caesar was a Roman general and statesman who played a critical role in the events that led to the demise of the Roman Republic and the rise of the Roman Empire."},
    
    {"text_input": "What caused the fall of the Roman Empire?", 
     "output": "The fall of the Roman Empire in 476 AD was due to a combination of internal decay and external pressures from invading barbarian tribes."},
    
    {"text_input": "Tell me about the Industrial Revolution.", 
     "output": "The Industrial Revolution, beginning in the 18th century, was a period of significant technological advancement that shifted economies from agrarian to industrial."},
    
    {"text_input": "What was the Cold War?", 
     "output": "The Cold War was a geopolitical tension between the Soviet Union and the United States and their respective allies after World War II, lasting from 1947 to 1991."},
    
    {"text_input": "Who was Cleopatra?", 
     "output": "Cleopatra VII was the last active ruler of the Ptolemaic Kingdom of Egypt, known for her intelligence, political acumen, and relationships with Roman leaders Julius Caesar and Mark Antony."},
]

# Fine-tune the model for the historian persona
operation = genai.create_tuned_model(
    # Model name for the fine-tuned model
    display_name="historian_chatbot",
    # Base model to fine-tune
    source_model=base_model,
    # number of times the model will see the training data
    epoch_count=20,
    # number of training examples to process in a single step
    batch_size=4,
    # learning rate for the fine-tuning operation
    learning_rate=0.001,
    # training data for fine-tuning
    training_data=training_data,
)

# Waiting for the fine-tuning operation to complete
for status in operation.wait_bar():
    time.sleep(10)

# Load the tuned model for use
result = operation.result()
model = genai.GenerativeModel(model_name=result.name)

# Function to check if the response is historical
def is_historical_response(response_text):
    keywords = ["history", "century", "AD", "BC", "revolution", "war", "empire", "king", "queen", "historical", "ancient", "dynasty"]
    for word in keywords:
        if word.lower() in response_text.lower():
            return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    if user_message:
        response = model.generate_content(user_message)
        # Check if the response is related to history, else give a default answer
        if is_historical_response(response.text):
            return jsonify({'reply': response.text})
        else:
            return jsonify({'reply': "I'm afraid I don't know enough about this field. Let's stick to historical topics!"})
    return jsonify({'reply': 'Sorry, I did not understand that.'}), 400

if __name__ == '__main__':
    app.run(debug=True)