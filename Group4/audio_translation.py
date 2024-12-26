import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import os

class AudioTranslation:
    def __init__(self, frame,show_home_callback):
        self.frame = frame
        self.show_home_callback = show_home_callback
        self.api_key = os.getenv("OPENAI_API_KEY")  # Fetch API key from environment
        if not self.api_key:
            raise ValueError("API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
        openai.api_key = self.api_key
        self.setup_ui()

    def setup_ui(self):
        # Consistent background and text color
        frame_bg = "#1a1a2e"  # Dark blue background
        label_fg = "white"    # White text color

        # Title Label
        tk.Label(
            self.frame,
            text="Audio Translation",
            font=("Arial", 18, "bold"),
            bg=frame_bg,
            fg=label_fg
        ).pack(pady=20)

        # Select File Button
        tk.Button(
            self.frame,
            text="Select Audio File",
            command=self.upload_audio,
            font=("Arial", 12),
            bg="white",
            fg="#e94560",  # Red text for contrast
            activebackground="#f0f0f0",
            activeforeground="#e94560",
            relief="flat",
            bd=0
        ).pack(pady=10)

        # Display Translated Text
        self.audio_text = tk.Text(
            self.frame,
            height=10,
            width=60,
            bg="white",  # White text area background
            fg="black",  # Black text color for readability
            wrap="word"  # Wrap text for better formatting
        )
        self.audio_text.pack(pady=10)

        # Back to Home Button
        tk.Button(
            self.frame,
            text="Back to Home",
            command=lambda: self.show_home_callback("Home"),
            font=("Arial", 12),
            bg="white",
            fg="#e94560",
            activebackground="#f0f0f0",
            activeforeground="#e94560",
            relief="flat",
            bd=0
        ).pack(pady=20)

    def upload_audio(self):
        # Open file dialog to select an audio file
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
        if not file_path:
            return

        try:
            # Translate audio using Whisper API
            translated_text = self.translate_audio(file_path)

            # Display translated text in the text widget
            self.audio_text.delete("1.0", "end")
            self.audio_text.insert("1.0", translated_text)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def translate_audio(self, file_path):
        # Use OpenAI Whisper API to translate audio
        try:
            with open(file_path, "rb") as audio_file:
                response = openai.audio.translations.create(
                    model="whisper-1",  # Whisper model
                    file=audio_file
                )
            # Convert the response to string and clean up the `Translation(text=)` part
            response_string = str(response)
            if "Translation(text=" in response_string:
                # Extract the text and remove the wrapper and quotes
                translated_text = response_string.split("Translation(text=")[1].rstrip(")").strip('"')
            else:
                # If no wrapper, use the string and strip quotes
                translated_text = response_string.strip('"')

            if not translated_text:
                raise ValueError("No text returned from the Whisper API.")
            
            return translated_text.strip()  # Remove extra spaces or newlines
        except Exception as e:
            raise Exception(f"Failed to translate audio: {e}")
