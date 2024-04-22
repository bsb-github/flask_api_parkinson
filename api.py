from flask import Flask, request, jsonify
import openai
import speech_recognition as sr
from dotenv import load_dotenv
load_dotenv()
import os
openai.api_key = os.environ.get('OPENAI_API_KEY')
recognizer = sr.Recognizer()
from gtts import gTTS
client = openai.OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
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

@app.route('/')
def hello():
    return "Hello, welcome to the Flask API!"

sentences = [
    "Peter Piper picked a peck of pickled peppers.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
    "She sells seashells by the seashore.",
    "The quick brown fox jumps over the lazy dog."
]



@app.route('/speech_exercise', methods=['POST'])
def speech_exercise():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Start exercise
    exercise_results = []
    for sentence in sentences:
        tts = gTTS("Repeat the following sentence: " + sentence, lang='en')
        tts.save("prompt.mp3")
        os.system("mpg123 prompt.mp3")

        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        try:
            user_response = recognizer.recognize_google(audio)
            if user_response.lower() == sentence.lower():
                response_text = "Good job! Your speech was clear."
                exercise_results.append({"sentence": sentence, "result": response_text})
            else:
                response_text = "Try again. Your speech wasn't clear."
                exercise_results.append({"sentence": sentence, "result": response_text})
        except sr.UnknownValueError:
            response_text = "Sorry, I couldn't understand what you said."
            exercise_results.append({"sentence": sentence, "result": response_text})
        except sr.RequestError as e:
            response_text = "Could not request results from Google Speech Recognition service; {0}".format(e)
            exercise_results.append({"sentence": sentence, "result": response_text})

    return jsonify({"exercise_results": exercise_results})

if __name__ == '__main__':
     app.run(host='0.0.0.0', debug=True)
