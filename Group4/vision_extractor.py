import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import openai
import base64
import os


class VisionExtractor:
    def __init__(self, frame, show_frame=None):
        """
        Initialize the VisionExtractor tool.
        :param frame: The frame where the UI elements will be added.
        :param show_frame: Callback function to navigate between frames.
        """
        self.frame = frame
        self.show_frame = show_frame
        self.api_key = os.getenv("OPENAI_API_KEY")  # Fetch API key from environment
        if not self.api_key:
            raise ValueError("API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
        openai.api_key = self.api_key
        self.setup_ui()

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import openai
import base64
import os


class VisionExtractor:
    def __init__(self, frame, show_frame=None):
        """
        Initialize the VisionExtractor tool.
        :param frame: The frame where the UI elements will be added.
        :param show_frame: Callback function to navigate between frames.
        """
        self.frame = frame
        self.show_frame = show_frame
        self.api_key = os.getenv("OPENAI_API_KEY")  # Fetch API key from environment
        if not self.api_key:
            raise ValueError("API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
        openai.api_key = self.api_key
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the UI components for the VisionExtractor tool.
        """
        # Label to display selected image
        self.img_label = tk.Label(
            self.frame,
            text="Image will appear here",
            font=("Arial", 12),
            bg="#1a1a2e",  # Matches the frame's background color
            fg="white"  # White text for better contrast
        )
        self.img_label.pack(pady=10)

        # Text field to display extracted text
        self.text_label = tk.Label(
            self.frame,
            text="Extracted CAPTCHA text will appear here.",
            font=("Arial", 14),
            bg="#1a1a2e",  # Matches the frame's background color
            fg="white"  # White text for better contrast
        )
        self.text_label.pack(pady=10)

        # Button to select and process image
        self.select_button = tk.Button(
            self.frame,
            text="Select CAPTCHA Image",
            command=self.select_and_process_image,
            font=("Arial", 12),
            bg="white",
            fg="#e94560",  # Red text for contrast
            activebackground="#f0f0f0",
            activeforeground="#e94560",
            relief="flat",
            bd=0,
        )
        self.select_button.pack(pady=10)

        # Button to navigate back to the Home screen
        if self.show_frame:
            tk.Button(
                self.frame,
                text="Back to Home",
                command=lambda: self.show_frame("Home"),
                font=("Arial", 12),
                bg="white",
                fg="#e94560",  # Red text for contrast
                activebackground="#f0f0f0",
                activeforeground="#e94560",
                relief="flat",
                bd=0,
            ).pack(pady=10)

    def extract_text_from_captcha(self, image_path):
        """
        Extract text from the provided image using OpenAI GPT-4.
        :param image_path: Path to the image file.
        :return: Extracted text or an error message.
        """
        try:
            # Convert the image file to a Base64-encoded string
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()
                base64_image = base64.b64encode(image_bytes).decode("utf-8")  # Encode to Base64 and decode to string

            # Call the OpenAI API to extract text from the image
            response = openai.ChatCompletion.create(
                model="gpt-4-0314",
                messages=[
                    {
                        "role": "user",
                        "content": f"What’s on this image? Write the text only. Image Base64:\n{base64_image}",
                    }
                ],
                max_tokens=50,
            )
            # Extract and return the text from the response
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Error extracting text: {e}"

    def select_and_process_image(self):
        """
        Open a file dialog to select an image, process it, and display the extracted text.
        """
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if not file_path:
            return

        try:
            # Display the image in the Tkinter window
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Resize the image for display
            img_tk = ImageTk.PhotoImage(img)
            self.img_label.config(image=img_tk, text="", bg="#1a1a2e")  # Ensure background consistency
            self.img_label.image = img_tk

            # Extract text from the image
            captcha_text = self.extract_text_from_captcha(file_path)
            self.text_label.config(text=f"Extracted CAPTCHA: {captcha_text}")
        except Exception as e:
            self.text_label.config(text=f"Error: {e}")

    def extract_text_from_captcha(self, image_path):
        """
        Extract text from the provided image using OpenAI GPT-4.
        :param image_path: Path to the image file.
        :return: Extracted text or an error message.
        """
        try:
            # Convert the image file to a Base64-encoded string
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()
                base64_image = base64.b64encode(image_bytes).decode("utf-8")  # Encode to Base64 and decode to string

            # Call the OpenAI API to extract text from the image
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s on this image? Write the text only"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
                ],
                max_tokens=50,
            )
            # Extract and return the text from the response
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Error extracting text: {e}"

    def select_and_process_image(self):
        """
        Open a file dialog to select an image, process it, and display the extracted text.
        """
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if not file_path:
            return

        try:
            # Display the image in the Tkinter window
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Resize the image for display
            img_tk = ImageTk.PhotoImage(img)
            self.img_label.config(image=img_tk, text="")
            self.img_label.image = img_tk

            # Extract text from the image
            captcha_text = self.extract_text_from_captcha(file_path)
            self.text_label.config(text=f"Extracted CAPTCHA: {captcha_text}")
        except Exception as e:
            self.text_label.config(text=f"Error: {e}")
