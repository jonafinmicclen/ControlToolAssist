import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Visualiser:
    def __init__(self, root, x_data, y_data):
        self.root = root
        self.root.title("Interactive Plot")
        self.root.geometry("600x400")
        self.x_data = x_data
        self.y_data = y_data

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
        x_data = self.x_data
        y_data = self.y_data

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
            # Update the y-coordinate of the clicked point to the cursor's y-coordinate
            x_clicked, y_clicked = event.xdata, event.ydata
            index_clicked = (np.abs(np.array(self.plot.get_xdata()) - x_clicked)).argmin()

            # Set the y-coordinate of the clicked point to the cursor's y-coordinate
            y_data = self.plot.get_ydata()
            y_data[index_clicked] = y_clicked

            # Clear the current axis
            self.axis.clear()

            # Replot the entire dataset
            self.plot, = self.axis.plot(self.plot.get_xdata(), y_data, marker='o', linestyle='-', color='b')
            self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = Visualiser(root)
    root.mainloop()
