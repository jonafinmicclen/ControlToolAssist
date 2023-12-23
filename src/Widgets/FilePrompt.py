import tkinter as tk
from tkinter import filedialog

def open_file_entry_prompt():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create a StringVar to store the file path
    file_path_var = tk.StringVar()

    # Create an entry widget to display the selected file path
    file_path_entry = tk.Entry(root, width=40, textvariable=file_path_var)
    file_path_entry.pack(pady=20)

    # Create a button to open the file dialog
    browse_button = tk.Button(root, text="Browse", command=lambda: browse_file(file_path_var))
    browse_button.pack(pady=10)

    # Create a button to get the entered file path
    get_path_button = tk.Button(root, text="Get File Path", command=root.destroy)
    get_path_button.pack(pady=10)

    root.mainloop()

    # Return the selected file path after the window is closed
    return file_path_var.get()

def browse_file(file_path_var):
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
    if file_path:
        file_path_var.set(file_path)