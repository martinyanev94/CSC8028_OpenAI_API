import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import os

class QuestionGenerator:
    def __init__(self, frame,show_home_callback):
        self.frame = frame
        self.show_home_callback = show_home_callback
        self.api_key = os.getenv("OPENAI_API_KEY")  # Fetch API key from environment
        if not self.api_key:
            raise ValueError("API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
        openai.api_key = self.api_key
        self.setup_ui()

    def setup_ui(self):
        # Title Label
        tk.Label(self.frame, text="Question Generator", font=("Arial", 18)).pack(pady=20)
        
        # Select File Button
        tk.Button(self.frame, text="Select Text File", command=self.upload_text_file).pack(pady=10)
        
        # Generated Questions Display
        self.question_text = tk.Text(self.frame, height=10, width=60)
        self.question_text.pack(pady=10)
        tk.Button(self.frame, text="Back to Home", command=lambda: self.show_home_callback("Home")).pack(pady=20)

    def upload_text_file(self):
        # Open file dialog to select a text file
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return

        try:
            # Read the content of the file
            with open(file_path, "r") as file:
                text_content = file.read()

            # Generate questions using ChatGPT API
            questions = self.generate_questions_from_text(text_content)

            # Display generated questions in the text widget
            self.question_text.delete("1.0", "end")
            self.question_text.insert("1.0", questions)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def generate_questions_from_text(self, text_content):
        # Use OpenAI Chat API to generate questions
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant that generates questions from provided text."},
                    {"role": "user", "content": f"Generate questions based on the following text:\n\n{text_content}"}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()

        except Exception as e:
            raise Exception(f"Failed to generate questions: {e}")
