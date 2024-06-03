from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
from spellchecker import SpellChecker

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

spell = SpellChecker()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image = Image.open(file.stream)
        text = pytesseract.image_to_string(image)

        # Split the text into words
        words = text.split()
        misspelled = spell.unknown(words)

        # Prepare a response with corrections
        corrections = {word: spell.correction(word) for word in misspelled}

        return jsonify({"text": text, "corrections": corrections})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
