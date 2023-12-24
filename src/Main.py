import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Widgets import InputVisualiser, FilePrompt
import PIL
from Macro import MacroTool
from Config import config

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Control Tool Assist")
        self.geometry("300x400")

        self.load_gui()
        self.config = config.Config()
        
    def load_gui(self):

        start_recording_button = ttk.Button(self, text="Start Recording", command=self.start_recording)
        start_recording_button.pack(pady=20)

        stop_recording_button = ttk.Button(self, text="Stop Recording", command=self.stop_recording)
        stop_recording_button.pack(pady=20)

        save_button = ttk.Button(self, text="Save", command=self.save)
        save_button.pack(pady=20)

        create_new_button = ttk.Button(self, text="Create New Macro", command=self.create_new)
        create_new_button.pack(pady=20)

        play_button = ttk.Button(self, text="Play Loaded Macro", command=self.play)
        play_button.pack(pady=20)

        load_button = ttk.Button(self, text="Load Macro", command=self.load)
        load_button.pack(pady=20)

    def start_recording(self):
        self.LoadedMacro.start_recording()

    def stop_recording(self):
        self.LoadedMacro.stop_recording()

    def save(self):
        self.LoadedMacro.save()
    
    def play(self):
        self.LoadedMacro.play()

    def load(self):
        fileDirectory = FilePrompt.open_file_entry_prompt()
        self.LoadedMacro = MacroTool.MacroTool.load(fileDirectory)
        pass

    def create_new(self):
        self.LoadedMacro = MacroTool.MacroTool(self.config.controler_polling_rate, self.config.screen_polling_rate)
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()