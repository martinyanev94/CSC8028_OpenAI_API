import tkinter as tk
from vision_extractor import VisionExtractor
from audio_translation import AudioTranslation
from resume_builder import ResumeBuilder
from question_generator import QuestionGenerator
from grammar_fixer import GrammarFixer

class AIToolkitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Toolkit")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a2e")  # Set consistent background color

        # Create a dictionary to hold frames
        self.frames = {}

        # Create frames for each tool
        tools = {
            "Vision Extractor": VisionExtractor,
            "Audio Translation": AudioTranslation,
            "Resume Builder": ResumeBuilder,
            "Question Generator": QuestionGenerator,
            "Grammar Fixer": GrammarFixer,
        }

        for tool_name, tool_class in tools.items():
            frame = tk.Frame(self.root, bg="#1a1a2e")
            self.frames[tool_name] = frame
            tool_class(frame, self.show_frame)
            frame.grid(row=0, column=0, sticky="nsew")

        # Add the home screen
        self.setup_home()
        self.frames["Home"].grid(row=0, column=0, sticky="nsew")
        self.show_frame("Home")

    def show_frame(self, name):
        """Raise the specified frame to the top."""
        frame = self.frames[name]
        frame.tkraise()

    def setup_home(self):
        """Set up the Home screen with buttons linking to other tools."""
        frame = tk.Frame(self.root, bg="#1a1a2e")
        self.frames["Home"] = frame

        # Header
        tk.Label(
            frame,
            text="Welcome to the AI Toolkit!",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#e94560",  # Red header background
            padx=10,
            pady=10,
        ).pack(pady=20)

        # Buttons for each tool
        tools = [
            ("Vision Extractor", "Vision Extractor"),
            ("Audio Translation", "Audio Translation"),
            ("Resume Builder", "Resume Builder"),
            ("Question Generator", "Question Generator"),
            ("Grammar Fixer", "Grammar Fixer"),
        ]

        for tool_name, tool_key in tools:
            tk.Button(
                frame,
                text=tool_name,
                command=lambda t=tool_key: self.show_frame(t),  # Navigate to the corresponding frame
                width=25,
                font=("Arial", 12, "bold"),
                bg="white",
                fg="#e94560",  # Red text color
                activebackground="#f0f0f0",  # Light background on hover
                activeforeground="#e94560",
                relief="flat",  # Flat style for a cleaner look
                bd=0,  # Remove border
            ).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = AIToolkitApp(root)
    root.mainloop()
