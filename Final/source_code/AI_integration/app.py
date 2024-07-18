from PIL import Image
from io import BytesIO
from api import gemini_api

import google.generativeai as genai
from flask import Flask, request, render_template

genai.configure(api_key=gemini_api())
model = genai.GenerativeModel('gemini-1.5-flash')
app = Flask(__name__)

def prompt(message):
    return f"Sử dụng hình ảnh dashboard ở trên để trả lời câu hỏi bên dưới:\n\nCâu hỏi: {message}"

chat = model.start_chat()
image = Image.open('Dashboard.png')
chat.send_message([prompt(''), image])

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_response', methods=['POST'])
def get_response():
    message = request.json.get('message')

    # screenshot = request.json.get('screenshot')
    
    print(f"User Input: {message}")
    # print(f"Screenshot: {screenshot}")

    # screenshot_data = base64.b64decode(screenshot.split(',')[1])
    # with open('screenshot__.png', 'wb') as f:
    #     f.write(screenshot_data)
    # image = Image.open(BytesIO(screenshot_data))
    # image.save('screenshot.png')

    response = chat.send_message(prompt(message))
    return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
