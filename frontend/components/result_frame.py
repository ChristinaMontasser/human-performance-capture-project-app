

import tkinter as tk
import os

class ResultFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        

        self.label = tk.Label(self, text="Model Output Results")
        self.label.pack(pady=10)
        
        self.result_text = tk.Text(self, wrap="word", height=10, width=50)
        self.result_text.pack(pady=10)

        self.open_folder_button = tk.Button(self, text="Open Results Folder", command=self.open_folder)
        self.open_folder_button.pack(pady=10)

    def display_results(self, result, folder_path):
        self.folder_path = folder_path

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
#        self.result_text.insert("1.0", result)
        self.result_text.insert("end", "\n\nProcess has successfully completed. Please check the folder.")
        self.result_text.config(state="disabled")

    def open_folder(self):
        # Open the folder in the file explorer
        if os.path.isdir(self.folder_path):
            os.startfile(self.folder_path)  # This works on Windows

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Model Output Results")