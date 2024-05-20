import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Load Gemini API key (securely!)
api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=api_key)

@app.route('/chat', methods=['POST'])
def bot():
    user_message = request.json['user_input']
    topic = "you are expert on parkinson disease, give answer in the form of paragraph also restrict your answer to 50 words"  # Specify your topic

    prompt = f"""{topic}. 
    Please answer the following question: 
    {user_message}"""
    # Gemini interaction (simplified)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    bot_response = response.text

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
