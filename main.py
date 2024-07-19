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



@app.route('/', methods=['POST','GET'])
def root():
    data = request.get_json()
    user_input = data.get('txt')
    image = data.get('image', None)
    history = data.get('history', [])
    rules = data.get('rules')
    
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=rules
    )
    
    chat_session = model.start_chat(history=history)
    try:
        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        print(e)
        return "Let's not talk about that."

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
