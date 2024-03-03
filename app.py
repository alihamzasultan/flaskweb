from flask import Flask, render_template, request, jsonify
import base64
from PIL import Image
from io import BytesIO
import google.generativeai as genai

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyCGTrhvJOJQmeBJtYvlQxmyFpw4TuloCHU"
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the file is included in the request
        if 'file' not in request.files:
            return 'Please upload an image and click "Solve".'

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return 'Please upload an image and click "Solve".'

        # Read the contents of the file and process it
        contents = file.read()
        img = parse_contents(contents)
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([
            "Given the uploaded image, which is expected to contain educational material such as multiple-choice questions (MCQs), fill in the blanks, true/false statements, or other questioning formats in any language, your task is to provide accurate and relevant answers. Please analyze the content within the image and generate responses accordingly. If the image does not contain relevant educational questioning content or if it contains invalid information, please acknowledge this in your response. Ensure that your answers are clear and concise.",
            img
        ])
        return jsonify({'response': response.text})

    return render_template('index.html')

def parse_contents(contents):
    img = Image.open(BytesIO(contents))
    return img

if __name__ == '__main__':
    app.run(debug=True)
