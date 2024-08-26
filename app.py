from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load your trained language detection model
with open("D:/Data/PU/Semester_3/NlpProject/Nlp1/model_nlp1.pkl", 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Language Detection</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 50px;
                text-align: center;
            }

            input[type="text"] {
                width: 300px;
                padding: 10px;
                margin: 20px;
            }

            button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }

            button:hover {
                background-color: #45a049;
            }

            .result {
                margin-top: 20px;
                font-size: 1.2em;
            }
        </style>
    </head>
    <body>

        <h1>Language Detection</h1>
        <input type="text" id="textInput" placeholder="Enter text or sentence here">
        <button onclick="detectLanguage()">Detect Language</button>

        <div class="result" id="result"></div>

        <script>
            function detectLanguage() {
                const text = document.getElementById('textInput').value;
                if (text.trim() === '') {
                    document.getElementById('result').textContent = 'Please enter a text or sentence.';
                    return;
                }

                fetch('/detect_language', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text }),
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').textContent = 'Detected Language: ' + data.language;
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('result').textContent = 'An error occurred while detecting the language.';
                });
            }
        </script>

    </body>
    </html>
    '''

@app.route('/detect_language', methods=['POST'])
def detect_language():
    data = request.get_json()
    text = data.get('text')

    # Predict the language using your ML model
    detected_language = model.predict([text])[0]

    return jsonify({'language': detected_language})

if __name__ == '__main__':
    app.run(debug=True)
