import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import os

class ResumeBuilder:
    def __init__(self, frame,show_home_callback):
        self.frame = frame
        self.show_home_callback = show_home_callback
        self.api_key = os.getenv("OPENAI_API_KEY")  
        if not self.api_key:
            raise ValueError("API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
        openai.api_key = self.api_key
        self.setup_ui()

    def setup_ui(self):
        # Consistent background color
        frame_bg = "#1a1a2e"  # Dark blue
        label_fg = "white"    # White text color for labels

        # Header
        tk.Label(
            self.frame,
            text="Resume Builder",
            font=("Arial", 18, "bold"),
            bg=frame_bg,
            fg=label_fg
        ).pack(pady=20)

        # Job Description Label
        tk.Label(
            self.frame,
            text="Enter Job Description:",
            bg=frame_bg,
            fg=label_fg
        ).pack()

        # Job Description Text Input
        self.job_description_input = tk.Text(
            self.frame,
            height=5,
            width=50,
            bg="white",   # White input background
            fg="black"    # Black text color for input
        )
        self.job_description_input.pack(pady=10)

        # Generate Resume Button
        tk.Button(
            self.frame,
            text="Generate Resume",
            command=self.generate_resume,
            bg="white",
            fg="#e94560",  # Red text for contrast
            activebackground="#f0f0f0",
            activeforeground="#e94560",
            relief="flat",
            bd=0,
        ).pack(pady=10)

        # Generated Resume Label
        tk.Label(
            self.frame,
            text="Generated Resume:",
            bg=frame_bg,
            fg=label_fg
        ).pack()

        # Generated Resume Text Output
        self.resume_output = tk.Text(
            self.frame,
            height=15,
            width=50,
            bg="white",   # White output background
            fg="black"    # Black text color for output
        )
        self.resume_output.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(self.frame, bg=frame_bg)
        button_frame.pack(pady=10)

        # Save Resume Button
        tk.Button(
            button_frame,
            text="Save Resume",
            command=self.save_resume,
            bg="white",
            fg="#e94560",
            activebackground="#f0f0f0",
            activeforeground="#e94560",
            relief="flat",
            bd=0,
        ).grid(row=0, column=0, padx=5)

        # Clear Button
        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all,
            bg="white",
            fg="#e94560",
            activebackground="#f0f0f0",
            activeforeground="#e94560",
            relief="flat",
            bd=0,
        ).grid(row=0, column=1, padx=5)

        # Back to Home Button
        tk.Button(
            self.frame,
            text="Back to Home",
            command=lambda: self.show_home_callback("Home"),
            bg="white",
            fg="#e94560",
            activebackground="#f0f0f0",
            activeforeground="#e94560",
            relief="flat",
            bd=0,
        ).pack(pady=20)

    def generate_resume(self):
        job_description = self.job_description_input.get("1.0", "end-1c").strip()
        if not job_description:
            messagebox.showwarning("Input Error", "Please enter a job description.")
            return
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional resume writer."},
                    {"role": "user", "content": f"Create a professional resume based on the following job description:\n\n{job_description}"}
                ]
            )
            generated_resume = response["choices"][0]["message"]["content"].strip()
            self.resume_output.delete("1.0", "end")
            self.resume_output.insert("1.0", generated_resume)
        except Exception as e:
            messagebox.showerror("API Error", f"An error occurred: {e}")

    def save_resume(self):
        resume_content = self.resume_output.get("1.0", "end-1c").strip()
        if not resume_content:
            messagebox.showwarning("Save Error", "No resume content to save.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(resume_content)
            messagebox.showinfo("Success", f"Resume saved to {file_path}")

    def clear_all(self):
        self.job_description_input.delete("1.0", "end")
        self.resume_output.delete("1.0", "end")