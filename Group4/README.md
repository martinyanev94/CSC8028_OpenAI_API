# AI Toolkit

The **AI Toolkit** is a desktop application built with Python and Tkinter, leveraging OpenAI's API for various AI-powered tools. This application integrates features like text extraction from images, audio translation, grammar correction, resume generation, and question generation.

## Features

1. **Vision Extractor**:
   - Extracts text from images using OpenAI API.
   - Handles image uploads and displays extracted text.

2. **Audio Translation**:
   - Transcribes audio files using OpenAI's Whisper API.
   - Supports `.mp3` and `.wav` file formats.
   - Provides an easy-to-use interface for uploading files and viewing transcriptions directly in the app.

3. **Resume Builder**:
   - Generates professional resumes based on user-provided job descriptions.
   - Outputs resumes in a clean, readable format for downloading or copying.
   - Helps automate the process of tailoring resumes to specific roles.

4. **Question Generator**:
   - Generates questions from uploaded text files using OpenAI's GPT API.
   - Useful for educators, interview preparation, and study material creation.
   - Supports `.txt` file uploads and displays generated questions in the app interface.

5. **Grammar Fixer**:
   - Corrects grammar in text files and provides downloadable corrected versions.

## Requirements

- Python 3.7+
- OpenAI API Key (Set as an environment variable)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/martinyanev94/ChatGPT_Group4.git
   cd ChatGPT_Group4


1. **Install required dependencies**:
   ```bash
   pip3 install -r requirements.txt   
   ```

2.Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

3.Run the application:

```bash
   python3 main.py
```