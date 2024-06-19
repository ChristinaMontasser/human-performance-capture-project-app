import tkinter as tk
from tkinter import filedialog, messagebox
import requests

class UploadFrame(tk.Frame):
    def __init__(self, parent, show_result_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.show_result_callback = show_result_callback
        
        self.label = tk.Label(self, text="Choose an image...")
        self.label.pack(pady=10)
        
        self.upload_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.upload_button.pack(pady=10)
        
        self.model_label = tk.Label(self, text="Select model")
        self.model_label.pack(pady=10)
        
        self.model_var = tk.StringVar(value="model1")
        self.model_dropdown = tk.OptionMenu(self, self.model_var, "model1", "model2", "model3")
        self.model_dropdown.pack(pady=10)
        
        self.submit_button = tk.Button(self, text="Upload", command=self.upload_image)
        self.submit_button.pack(pady=20)
        
        self.file_path = None

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if self.file_path:
            self.label.config(text=f"Selected file: {self.file_path}")
        
    def upload_image(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return
        
        model = self.model_var.get()
        try:
            with open(self.file_path, 'rb') as image_file:
                files = {'image': image_file}
                data = {'model': model}
                response = requests.post("http://localhost:5000/api/upload", files=files, data=data)
                
                if response.status_code == 200:
                    self.show_result_callback(response.json())
                else:
                    messagebox.showerror("Error", f"Failed to upload image: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Upload Image for Parameter Estimation")
    UploadFrame(root, lambda x: print(x)).pack(fill="both", expand=True)
    root.mainloop()
