from flask import Flask, request
import os
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route('/', methods=['POST','GET'])
def root():
    data = request.json
    user_input = request.args.get('txt')
    
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)
    
    return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
