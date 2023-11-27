import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class InteractivePlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Plot")
        self.root.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        # Create a Matplotlib figure and axis
        self.figure, self.axis = Figure(), None  # Will be set during plot initialization

        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Create a button to toggle interaction mode
        self.interaction_button = ttk.Button(self.root, text="Toggle Interaction", command=self.toggle_interaction)
        self.interaction_button.pack()

        # Set up the initial plot
        self.plot_initial_data()

    def plot_initial_data(self):
        # Create initial data for plotting
        x_data = [1, 2, 3, 4, 5]
        y_data = [2, 4, 1, 7, 3]

        # Plot the initial data
        self.axis = self.figure.add_subplot(111)
        self.plot, = self.axis.plot(x_data, y_data, marker='o', linestyle='-', color='b')
        self.canvas.draw()

        # Set up event handling for interaction
        self.is_interactive = False
        self.canvas.mpl_connect('button_press_event', self.on_click)

    def toggle_interaction(self):
        # Toggle interaction mode
        self.is_interactive = not self.is_interactive
        if self.is_interactive:
            print("Interaction mode enabled. Click on the plot to move points.")
        else:
            print("Interaction mode disabled.")

    def on_click(self, event):
        # Handle click events when interaction mode is enabled
        if self.is_interactive and event.inaxes == self.axis:
            # Update the y-coordinate of the clicked point
            x_clicked, y_clicked = event.xdata, event.ydata
            index_clicked = (np.abs(np.array(self.plot.get_xdata()) - x_clicked)).argmin()

            # Update the y-coordinate of the clicked point
            self.plot.set_ydata(np.insert(self.plot.get_ydata(), index_clicked, y_clicked))

            # Redraw the canvas
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = InteractivePlotApp(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = InteractivePlotApp(root)
    root.mainloop()
