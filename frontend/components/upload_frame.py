import tkinter as tk
from tkinter import filedialog
# from utils.api import upload_image, run_modelss

class UploadFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()
        
        self.run_button = tk.Button(self, text="Run Model", command=self.run_model)
        self.run_button.pack()

    def upload_image(self):
        self.filepath = filedialog.askopenfilename()
        if self.filepath:
            self.upload_button.config(text="Image Uploaded")
    
    def run_model(self):
        if hasattr(self, 'filepath'):
            result = run_model(self.filepath)
            self.master.show_result_frame(result)

