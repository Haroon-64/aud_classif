import os
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, ttk
from seperator import separate_instruments_single_file
from tempfile import NamedTemporaryFile

class AudioSeparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Separator")
        
        self.themes = {
            "light": {
                "bg": "white",
                "fg": "black",
                "button_bg": "#5591f5",
                "button_fg": "white"
            },
            "dark": {
                "bg": "black",
                "fg": "white",
                "button_bg": "#c98bdb",
                "button_fg": "black"
            }
        }
        self.current_theme = "light"

        self.create_widgets()

    def create_widgets(self):
        self.upload_button = tk.Button(self.root, text="Upload Audio File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.output_format_label = tk.Label(self.root, text="Select Output Format")
        self.output_format_label.pack()

        self.output_format = ttk.Combobox(self.root, values=["mp3", "wav"])
        self.output_format.pack(pady=5)

        self.quality_label = tk.Label(self.root, text="Select Audio Quality")
        self.quality_label.pack()

        self.quality = ttk.Combobox(self.root, values=["128k", "192k", "256k", "320k"])
        self.quality.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start Separation", command=self.start_separation)
        self.start_button.pack(pady=20)

        self.theme_button = tk.Button(self.root, text="Change Theme", command=self.change_theme)
        self.theme_button.pack(pady=5)

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg")])
        if not self.file_path:
            return

    def change_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        theme = self.themes[self.current_theme]
        self.root.config(bg=theme["bg"])
        for widget in self.root.winfo_children():
            widget.config(bg=theme["bg"], fg=theme["fg"])
            if isinstance(widget, tk.Button):
                widget.config(bg=theme["button_bg"], fg=theme["button_fg"])

    def start_separation(self):
        if not hasattr(self, 'file_path'):
            messagebox.showwarning("Warning", "Please upload an audio file.")
            return

        output_format = self.output_format.get()
        quality = self.quality.get()

        if not output_format or not quality:
            messagebox.showwarning("Warning", "Please select output format and quality.")
            return

        with NamedTemporaryFile(delete=False) as temp_input_file:
            with open(self.file_path, 'rb') as f:
                temp_input_file.write(f.read())
                temp_input_file.flush()

            output_dir = os.path.join(os.getcwd(), 'output')
            os.makedirs(output_dir, exist_ok=True)

            messagebox.showinfo("Processing", "Processing...")
            output_path = separate_instruments_single_file(temp_input_file.name, output_dir, output_format, quality)

            messagebox.showinfo("Separation Complete", f"Output saved in {output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSeparatorApp(root)
    root.mainloop()
