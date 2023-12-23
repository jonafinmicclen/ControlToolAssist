import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import InputVisualiser
import pyautogui

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Controller Macro Tool")

        InputVisualiser.Visualiser([1,2,3],[1,1,1])

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()