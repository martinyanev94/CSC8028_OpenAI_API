import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import os

class GrammarFixer:
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
            text="Grammar Fixer",
            font=("Arial", 18, "bold"),
            bg=frame_bg,
            fg=label_fg
        ).pack(pady=20)

        # Select File Button
        tk.Button(
            self.frame,
            text="Select Text File",
            command=self.upload_text_file,
            font=("Arial", 12),
            bg="white",
            fg="#e94560",  # Red text for contrast
            activebackground="#f0f0f0",
            activeforeground="#e94560",
            relief="flat",
            bd=0
        ).pack(pady=10)

        # Text Widget to Display Corrected Text
        self.grammar_text = tk.Text(
            self.frame,
            height=15,
            width=60,
            bg="white",  # White text area background
            fg="black",  # Black text color for readability
            wrap="word"  # Wrap text for better formatting
        )
        self.grammar_text.pack(pady=10)

        # Save Corrected Text Button
        tk.Button(
            self.frame,
            text="Save Corrected Text",
            command=self.save_corrected_text,
            font=("Arial", 12),
            bg="white",
            fg="#e94560",
            activebackground="#f0f0f0",
            activeforeground="#e94560",
            relief="flat",
            bd=0
        ).pack(pady=10)

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
    def upload_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    original_text = file.read()

                # Use OpenAI ChatCompletion to correct grammar
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a grammar correction assistant."},
                        {"role": "user", "content": f"Correct the grammar of the following text:\n\n{original_text}"}
                    ]
                )
                corrected_text = response["choices"][0]["message"]["content"].strip()

                # Display corrected text in the Text widget
                self.grammar_text.delete("1.0", "end")
                self.grammar_text.insert("1.0", corrected_text)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def save_corrected_text(self):
        corrected_text = self.grammar_text.get("1.0", "end-1c").strip()
        if not corrected_text:
            messagebox.showwarning("Warning", "There is no corrected text to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(corrected_text)
                messagebox.showinfo("Success", f"Corrected text saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving: {e}")
