from flask import Flask, render_template, request, jsonify
import pytesseract
from PIL import Image
import openai
import easyocr
import io
import os

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Configure OpenAI API key
openai.api_key = '[API_KEY]'

# Vision Extractor (Captcha Text Recognition)
reader = easyocr.Reader(['en'])  # Add other languages if needed, e.g., ['en', 'es']

@app.route('/extract-text', methods=['POST'])
def extract_text():
    """
    Endpoint to extract text from an uploaded image.
    """
    file = request.files.get('image')
    if file:
        try:
            # Open and read the uploaded image file
            img = Image.open(file)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format=img.format)
            img_bytes = img_bytes.getvalue()

            # Perform OCR using EasyOCR
            result = reader.readtext(img_bytes, detail=0)  # detail=0 returns only text
            extracted_text = " ".join(result)  # Combine all extracted text into a single string

            # Return the extracted text as a JSON response
            return jsonify({"text": extracted_text}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No file uploaded"}), 400


# Audio Translator (Whisper API)


def translate_audio(file_path):
    """
    Transcribes an audio file using OpenAI's Whisper API.
    """
    try:
        with open(file_path, "rb") as audio_file:
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
        return response.get('text', "No transcription found.")
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/audio-translation', methods=['POST'])
def audio_translation():
    """
    Endpoint to handle audio translation.
    Accepts an audio file via POST request and returns the transcription as JSON.
    """
    file = request.files.get('file')
    if file:
        try:
            # Save the uploaded file to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Translate the audio using the Whisper API
            transcription = translate_audio(filepath)

            # Clean up the uploaded file (optional)
            os.remove(filepath)

            return jsonify({"transcription": transcription}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No file uploaded"}), 400


# Resume Builder
@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    job_desc = request.json.get('description')
    if job_desc:
        prompt = f"Generate a professional resume for this job description:\n{job_desc}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume generator."},
                {"role": "user", "content": prompt}
            ]
        )
        resume = response['choices'][0]['message']['content']
        return jsonify({"resume": resume.strip()})
    return jsonify({"error": "No job description provided"}), 400

# Question Generator
@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    text = request.json.get('text')
    if text:
        prompt = f"Create multiple-choice questions based on the following text:\n{text}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a question generator for educational purposes."},
                {"role": "user", "content": prompt}
            ]
        )
        questions = response['choices'][0]['message']['content']
        return jsonify({"questions": questions.strip()})
    return jsonify({"error": "No text provided"}), 400

# Grammar Fixer
@app.route('/fix-grammar', methods=['POST'])
def fix_grammar():
    bad_text = request.json.get('text')
    if bad_text:
        prompt = f"Fix the grammar of the following text:\n{bad_text}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a grammar corrector."},
                {"role": "user", "content": prompt}
            ]
        )
        fixed_text = response['choices'][0]['message']['content']
        return jsonify({"fixed_text": fixed_text.strip()})
    return jsonify({"error": "No text provided"}), 400

# Home route
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
