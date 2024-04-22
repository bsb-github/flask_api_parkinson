from flask import Flask, request, jsonify
import openai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
load_dotenv()
from os import environ
openai.api_key = environ.get('OPENAI_API_KEY')
recognizer = sr.Recognizer()
engine = pyttsx3.init()

client = openai.OpenAI(
    api_key=environ.get('OPENAI_API_KEY')
)
messages = [
    {"role": "system", "content": "You are in a session with a Parkinson's disease speech therapist. You can discuss any concerns or ask for assistance related to speech therapy. Please feel free to start the conversation."},
]

app = Flask(__name__)
def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['user_input']
    # Process user input and return bot response
    bot_response = chatbot(user_input)
    return jsonify({"bot_response": bot_response})



sentences = [
    "Peter Piper picked a peck of pickled peppers.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
    "She sells seashells by the seashore.",
    "The quick brown fox jumps over the lazy dog."
]



@app.route('/speech-exercise', methods=['POST'])
def speech_exercise():
    data = request.json
    if 'audio' not in data:
        return jsonify({'error': 'Audio data not provided'}), 400
    
    audio_data = data['audio']
    
    try:
        text = recognize_speech(audio_data)
        result = evaluate_response(text)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def recognize_speech(audio_data):
    with sr.AudioData(audio_data) as source:
        text = recognizer.recognize_google(source)
    return text.lower()

def evaluate_response(user_response):
    for sentence in sentences:
        if user_response.lower() == sentence.lower():
            return {'message': 'Good job! Your speech was clear.'}
    
    return {'message': 'Try again. Your speech wasn\'t clear.'}


if __name__ == '__main__':
     app.run(host='0.0.0.0', debug=True)
